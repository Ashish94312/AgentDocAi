
import subprocess
import json
import os
import time
from django.conf import settings

def mcp_tool(command_args: list[str]) -> dict or list or str or None:
    """
    Executes the MCP server directly with the given command arguments and returns the JSON response.
    This bypasses the problematic mcpcurl tool and communicates directly with the MCP server.
    """
    # Get the project root directory (parent of mcp_integration)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    github_mcp_server_path = os.path.join(project_root, 'github-mcp-server', 'github-mcp-server')
    
    # Parse the command to determine what tool to call
    if len(command_args) < 3 or command_args[0] != 'tools':
        print(f"Invalid command format: {command_args}")
        return None
    
    tool_name = command_args[1]
    
    # Build the MCP request
    mcp_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": {}
        }
    }
    
    # Parse arguments from command line format
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
            
            mcp_request["params"]["arguments"][arg_name] = arg_value
        else:
            i += 1
    
    print(f"mcp_tool executing MCP request: {json.dumps(mcp_request, indent=2)}")
    
    # Set environment variables
    env = os.environ.copy()
    env['GITHUB_PERSONAL_ACCESS_TOKEN'] = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    
    try:
        # Start the MCP server
        process = subprocess.Popen(
            [github_mcp_server_path, '--toolsets', 'repos,issues,pull_requests,code_security', 'stdio'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            bufsize=1
        )
        
        # Wait a moment for server to start
        time.sleep(1)
        
        # Send the request
        request_json = json.dumps(mcp_request) + '\n'
        process.stdin.write(request_json)
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        
        # Close the process
        process.terminate()
        process.wait()
        
        if response:
            try:
                response_data = json.loads(response)
                print(f"MCP response: {json.dumps(response_data, indent=2)}")
                
                # Check if it's an error response
                if 'error' in response_data:
                    print(f"MCP error: {response_data['error']}")
                    return None
                
                # Extract the result
                if 'result' in response_data:
                    result = response_data['result']
                    if 'content' in result and len(result['content']) > 0:
                        # The actual data is in content[0] for get_file_contents
                        content_item = result['content'][0]
                        if 'text' in content_item:
                            # Parse the text content which contains the actual data
                            try:
                                return json.loads(content_item['text'])
                            except json.JSONDecodeError:
                                return content_item['text']
                        else:
                            return content_item
                    elif 'text' in result:
                        # Some tools return text directly
                        try:
                            return json.loads(result['text'])
                        except json.JSONDecodeError:
                            return result['text']
                    else:
                        return result
                else:
                    return response_data
                    
            except json.JSONDecodeError as e:
                print(f"Failed to parse MCP response JSON: {e}")
                print(f"Raw response: {response}")
                return response.strip()
        else:
            print("No response from MCP server")
            return None

    except FileNotFoundError:
        print(f"Error: MCP server not found at {github_mcp_server_path}")
        print("Falling back to GitHub API...")
        # Fallback to GitHub API if MCP server is not available
        try:
            from .github_api import github_tool
            return github_tool(tool_name, **{arg: mcp_request["params"]["arguments"][arg] for arg in mcp_request["params"]["arguments"]})
        except ImportError:
            print("GitHub API fallback not available")
            return None
    except subprocess.TimeoutExpired:
        print("Error: Timeout communicating with MCP server.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while running MCP server: {e}")
        return None