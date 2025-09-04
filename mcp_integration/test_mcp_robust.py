#!/usr/bin/env python3
"""
Robust test of MCP server communication
"""
import json
import subprocess
import os
import sys
import time

def test_mcp_server_robust():
    # Set the GitHub token
    os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'] = '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'
    
    # Path to the MCP server
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mcp_server_path = os.path.join(project_root, 'github-mcp-server', 'github-mcp-server')
    
    print("=== Testing MCP Server with Robust Communication ===")
    
    try:
        # Start the MCP server process
        process = subprocess.Popen(
            [mcp_server_path, '--toolsets', 'repos,issues,pull_requests,code_security', 'stdio'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=os.environ,
            text=True,
            bufsize=1
        )
        
        # Wait a moment for server to start
        time.sleep(1)
        
        # Test 1: List tools
        print("\n--- Testing Tools List ---")
        tools_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        print(f"Sending request: {json.dumps(tools_request)}")
        process.stdin.write(json.dumps(tools_request) + '\n')
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        if response:
            print(f"Tools response: {response}")
            try:
                tools_data = json.loads(response)
                print("✅ Tools list successful!")
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
        else:
            print("❌ No response for tools list")
        
        # Test 2: Get file contents
        print("\n--- Testing Get File Contents ---")
        file_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_file_contents",
                "arguments": {
                    "owner": "microsoft",
                    "repo": "vscode",
                    "path": "/"
                }
            }
        }
        
        print(f"Sending request: {json.dumps(file_request)}")
        process.stdin.write(json.dumps(file_request) + '\n')
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        if response:
            print(f"File contents response: {response}")
            try:
                file_data = json.loads(response)
                print("✅ Get file contents successful!")
                
                # Extract the actual file structure data
                if 'result' in file_data and 'content' in file_data['result']:
                    content = file_data['result']['content']
                    if len(content) > 1:
                        file_structure = content[1]
                        print(f"File structure data: {json.dumps(file_structure, indent=2)}")
                    else:
                        print(f"Content structure: {content}")
                else:
                    print(f"Result structure: {file_data.get('result', 'No result')}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
        else:
            print("❌ No response for file contents")
        
        # Test 3: List branches
        print("\n--- Testing List Branches ---")
        branches_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "list_branches",
                "arguments": {
                    "owner": "microsoft",
                    "repo": "vscode",
                    "perPage": 5
                }
            }
        }
        
        print(f"Sending request: {json.dumps(branches_request)}")
        process.stdin.write(json.dumps(branches_request) + '\n')
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        if response:
            print(f"Branches response: {response}")
            try:
                branches_data = json.loads(response)
                print("✅ List branches successful!")
                
                # Extract the actual branches data
                if 'result' in branches_data and 'content' in branches_data['result']:
                    content = branches_data['result']['content']
                    if len(content) > 1:
                        branches = content[1]
                        print(f"Branches data: {json.dumps(branches, indent=2)}")
                    else:
                        print(f"Content structure: {content}")
                else:
                    print(f"Result structure: {branches_data.get('result', 'No result')}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
        else:
            print("❌ No response for branches")
        
        # Close the process
        process.terminate()
        process.wait()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'process' in locals():
            process.terminate()
        return False

if __name__ == "__main__":
    print("Testing MCP Server with Robust Communication")
    print("=" * 60)
    
    success = test_mcp_server_robust()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Test completed successfully!")
    else:
        print("❌ Test failed. Check the output above for details.")
