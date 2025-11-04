import subprocess
import json
import os
import asyncio
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
    
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": args}
    }
    
    env = os.environ.copy()
    env['GITHUB_PERSONAL_ACCESS_TOKEN'] = settings.GITHUB_PERSONAL_ACCESS_TOKEN
    
    try:
        proc = subprocess.Popen(
            [server_path, '--toolsets', 'repos,issues,pull_requests,code_security', 'stdio'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=env, text=True, bufsize=1
        )
        await asyncio.sleep(1)
        proc.stdin.write(json.dumps(request) + '\n')
        proc.stdin.flush()
        response = proc.stdout.readline()
        proc.terminate()
        proc.wait()
        
        if not response:
            return None
        
        data = json.loads(response)
        if 'error' in data:
            return None
        
        result = data.get('result', {})
        if 'content' in result and result['content']:
            item = result['content'][0]
            if 'text' in item:
                try:
                    return json.loads(item['text'])
                except:
                    return item['text']
            return item
        elif 'text' in result:
            try:
                return json.loads(result['text'])
            except:
                return result['text']
        return result
        
    except FileNotFoundError:
        try:
            from .github_api import github_tool
            return github_tool(tool_name, **args)
        except ImportError:
            return None
    except:
        return None

def mcp_tool_sync(command_args):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                return executor.submit(asyncio.run, mcp_tool(command_args)).result()
        return loop.run_until_complete(mcp_tool(command_args))
    except RuntimeError:
        return asyncio.run(mcp_tool(command_args))