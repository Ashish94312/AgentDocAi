import subprocess
import json
import os
import time
import threading
from typing import Dict, Any, Optional
from django.conf import settings
import hashlib
import pickle
from pathlib import Path

class MCPConnectionPool:
    """Connection pool for MCP servers to reduce subprocess overhead"""
    
    def __init__(self, max_connections=3):
        self.max_connections = max_connections
        self.connections = {}
        self.lock = threading.Lock()
        self.cache_dir = Path("/tmp/mcp_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
    def _get_cache_key(self, tool_name: str, arguments: dict) -> str:
        """Generate cache key for MCP calls"""
        cache_data = f"{tool_name}:{json.dumps(arguments, sort_keys=True)}"
        return hashlib.md5(cache_data.encode()).hexdigest()
    
    def _get_cached_result(self, cache_key: str) -> Optional[Any]:
        """Get cached result if available and not expired"""
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        if cache_file.exists():
            # Check if cache is less than 5 minutes old
            if time.time() - cache_file.stat().st_mtime < 300:  # 5 minutes
                try:
                    with open(cache_file, 'rb') as f:
                        return pickle.load(f)
                except (pickle.PickleError, EOFError):
                    cache_file.unlink()  # Remove corrupted cache
        return None
    
    def _cache_result(self, cache_key: str, result: Any):
        """Cache the result"""
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(result, f)
        except (pickle.PickleError, OSError):
            pass  # Ignore cache errors
    
    def _get_connection(self) -> subprocess.Popen:
        """Get or create an MCP connection"""
        thread_id = threading.get_ident()
        
        with self.lock:
            if thread_id in self.connections:
                return self.connections[thread_id]
            
            # Create new connection
            # Get the project root (AgentDocAi directory)
            current_file = os.path.abspath(__file__)
            # Go up: utils_optimized.py -> mcp_manager -> mcp_integration -> AgentDocAi
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
            github_mcp_server_path = os.path.join(project_root, 'github-mcp-server', 'github-mcp-server')
            
            # Verify the path exists
            if not os.path.exists(github_mcp_server_path):
                print(f"❌ MCP server not found at: {github_mcp_server_path}")
                print(f"📁 Project root: {project_root}")
                print(f"🔍 Looking for: {github_mcp_server_path}")
                # Try alternative paths
                alt_paths = [
                    os.path.join(project_root, 'github-mcp-server', 'github-mcp-server'),
                    os.path.join(project_root, 'github-mcp-server', 'cmd', 'github-mcp-server', 'github-mcp-server'),
                    '/Users/ashishkumar/AgentDocAi/github-mcp-server/github-mcp-server'
                ]
                for alt_path in alt_paths:
                    if os.path.exists(alt_path):
                        github_mcp_server_path = alt_path
                        print(f"✅ Found MCP server at: {github_mcp_server_path}")
                        break
                else:
                    print("❌ MCP server not found in any expected location")
                    raise FileNotFoundError(f"MCP server not found at {github_mcp_server_path}")
            
            env = os.environ.copy()
            env['GITHUB_PERSONAL_ACCESS_TOKEN'] = settings.GITHUB_PERSONAL_ACCESS_TOKEN
            
            process = subprocess.Popen(
                [github_mcp_server_path, '--toolsets', 'repos,issues,pull_requests,code_security', 'stdio'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=True,
                bufsize=1
            )
            
            # Wait for server to start
            time.sleep(0.5)
            
            self.connections[thread_id] = process
            return process
    
    def _close_connection(self):
        """Close the current thread's connection"""
        thread_id = threading.get_ident()
        with self.lock:
            if thread_id in self.connections:
                try:
                    self.connections[thread_id].terminate()
                    self.connections[thread_id].wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.connections[thread_id].kill()
                except Exception:
                    pass
                del self.connections[thread_id]
    
    def call_tool(self, tool_name: str, arguments: dict) -> Any:
        """Call MCP tool with caching and connection pooling"""
        # Check cache first
        cache_key = self._get_cache_key(tool_name, arguments)
        cached_result = self._get_cached_result(cache_key)
        if cached_result is not None:
            return cached_result
        
        # Build MCP request
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        try:
            process = self._get_connection()
            
            # Send request
            request_json = json.dumps(mcp_request) + '\n'
            process.stdin.write(request_json)
            process.stdin.flush()
            
            # Read response with timeout
            import select
            if hasattr(select, 'select'):  # Unix-like systems
                ready, _, _ = select.select([process.stdout], [], [], 30)  # 30 second timeout
                if ready:
                    response = process.stdout.readline()
                else:
                    raise subprocess.TimeoutExpired("MCP call", 30)
            else:  # Windows fallback
                response = process.stdout.readline()
            
            if response:
                try:
                    response_data = json.loads(response)
                    
                    if 'error' in response_data:
                        print(f"MCP error: {response_data['error']}")
                        return None
                    
                    # Extract result
                    if 'result' in response_data:
                        result = response_data['result']
                        if 'content' in result and len(result['content']) > 0:
                            content_item = result['content'][0]
                            if 'text' in content_item:
                                try:
                                    final_result = json.loads(content_item['text'])
                                except json.JSONDecodeError:
                                    final_result = content_item['text']
                            else:
                                final_result = content_item
                        elif 'text' in result:
                            try:
                                final_result = json.loads(result['text'])
                            except json.JSONDecodeError:
                                final_result = result['text']
                        else:
                            final_result = result
                        
                        # Cache the result
                        self._cache_result(cache_key, final_result)
                        return final_result
                    else:
                        return response_data
                        
                except json.JSONDecodeError as e:
                    print(f"Failed to parse MCP response JSON: {e}")
                    return response.strip()
            else:
                print("No response from MCP server")
                return None
                
        except subprocess.TimeoutExpired:
            print("Error: Timeout communicating with MCP server.")
            self._close_connection()
            return None
        except Exception as e:
            print(f"An unexpected error occurred while running MCP server: {e}")
            self._close_connection()
            return None
    
    def cleanup(self):
        """Clean up all connections"""
        with self.lock:
            for process in self.connections.values():
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                except Exception:
                    pass
            self.connections.clear()

# Global connection pool instance
_connection_pool = MCPConnectionPool()

def mcp_tool_optimized(command_args: list[str]) -> dict or list or str or None:
    """
    Optimized MCP tool with connection pooling and caching
    """
    if len(command_args) < 3 or command_args[0] != 'tools':
        print(f"Invalid command format: {command_args}")
        return None
    
    tool_name = command_args[1]
    
    # Parse arguments from command line format
    arguments = {}
    i = 2
    while i < len(command_args):
        if command_args[i].startswith('--'):
            arg_name = command_args[i][2:]  # Remove -- prefix
            if i + 1 < len(command_args) and not command_args[i + 1].startswith('--'):
                arg_value = command_args[i + 1]
                i += 2
            else:
                arg_value = True
                i += 1
            
            # Convert string values to appropriate types
            if arg_value == 'true':
                arg_value = True
            elif arg_value == 'false':
                arg_value = False
            elif arg_value.isdigit():
                arg_value = int(arg_value)
            elif arg_value.replace('.', '').isdigit() and arg_value.count('.') == 1:
                arg_value = float(arg_value)
            
            arguments[arg_name] = arg_value
        else:
            i += 1
    
    return _connection_pool.call_tool(tool_name, arguments)

def cleanup_mcp_connections():
    """Clean up MCP connections - call this when done"""
    _connection_pool.cleanup()
