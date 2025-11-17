import subprocess
import json
import os
import asyncio
import time
from django.conf import settings

async def mcp_tool(command_args):
    if len(command_args) < 3 or command_args[0] != 'tools':
        return None
    
    tool_name = command_args[1]
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    server_path = os.path.join(project_root, 'github-mcp-server', 'github-mcp-server')
    
    args = {}
    i = 2
    while i < len(command_args):
        if command_args[i].startswith('--'):
            key = command_args[i][2:]
            if i + 1 < len(command_args) and not command_args[i + 1].startswith('--'):
                val = command_args[i + 1]
                if val == 'true': val = True
                elif val == 'false': val = False
                elif val.isdigit(): val = int(val)
                elif val.replace('.', '', 1).isdigit(): val = float(val)
                args[key] = val
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            i += 1
    
    initialize_request = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "mcp-manager", "version": "1.0.0"}
        }
    }
    
    initialized_notification = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    
    tool_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": args}
    }
    
    env = os.environ.copy()
    env['GITHUB_PERSONAL_ACCESS_TOKEN'] = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    
    if not os.path.exists(server_path):
        print(f"MCP server not found at {server_path}")
        return None
    
    proc = subprocess.Popen(
        [server_path, '--toolsets', 'repos,issues,pull_requests,code_security', 'stdio'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env=env, text=True, bufsize=1
    )
    
    proc.stdin.write(json.dumps(initialize_request) + '\n')
    proc.stdin.flush()
    
    init_response = None
    timeout = 5
    start_time = time.time()
    while time.time() - start_time < timeout:
        line = proc.stdout.readline()
        if not line:
            break
        line = line.strip()
        if line:
            data = json.loads(line)
            if data.get('id') == 0:
                init_response = data
                break
    
    if not init_response:
        proc.kill()
        proc.wait()
        return None
    
    proc.stdin.write(json.dumps(initialized_notification) + '\n')
    proc.stdin.flush()
    
    time.sleep(0.1)
    
    proc.stdin.write(json.dumps(tool_request) + '\n')
    proc.stdin.flush()
    
    tool_response = None
    timeout = 25
    start_time = time.time()
    while time.time() - start_time < timeout:
        line = proc.stdout.readline()
        if not line:
            break
        line = line.strip()
        if line:
            data = json.loads(line)
            if data.get('id') == 1:
                tool_response = data
                break
            elif 'result' in data and 'error' not in data and data.get('id') != 0:
                tool_response = data
                break
    
    proc.stdin.close()
    proc.wait(timeout=5)
    
    if not tool_response:
        return None
    
    data = tool_response
    if 'error' in data:
        error_info = data.get('error', {})
        if isinstance(error_info, dict):
            error_msg = error_info.get('message', '')
        else:
            error_msg = str(error_info)
        print(f"MCP error: {error_msg}")
        return None
    
    result = data.get('result', {})
    if not result:
        return None
    
    if 'content' in result and result['content']:
        item = result['content'][0]
        if isinstance(item, dict) and 'text' in item:
            text = item['text']
            parsed = json.loads(text)
            return parsed
        return item
    elif 'text' in result:
        text = result['text']
        parsed = json.loads(text)
        return parsed
    elif isinstance(result, list):
        return result
    elif isinstance(result, dict):
        return result
    return result

def mcp_tool_sync(command_args):
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    result = new_loop.run_until_complete(mcp_tool(command_args))
    new_loop.close()
    return result