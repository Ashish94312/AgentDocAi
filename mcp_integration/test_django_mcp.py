#!/usr/bin/env python3
"""
Test MCP communication in Django-like environment
"""
import json
import subprocess
import os
import sys

def test_mcp_in_django_env():
    # Set the GitHub token
    os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'] = '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'
    
    # Path to the MCP server
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mcp_server_path = os.path.join(project_root, 'github-mcp-server', 'github-mcp-server')
    
    print("=== Testing MCP Server in Django-like Environment ===")
    
    # Test the exact same approach as utils.py
    mcp_request = {
        "jsonrpc": "2.0",
        "id": 1,
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
    
    print(f"Sending request: {json.dumps(mcp_request, indent=2)}")
    
    try:
        # Use communicate method which is more reliable
        process = subprocess.Popen(
            [mcp_server_path, '--toolsets', 'repos,issues,pull_requests,code_security', 'stdio'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=os.environ,
            text=True
        )
        
        # Send the request and wait for response
        request_json = json.dumps(mcp_request) + '\n'
        stdout, stderr = process.communicate(input=request_json, timeout=30)
        
        if stderr:
            print(f"MCP server stderr: {stderr}")
        
        if stdout:
            print(f"✅ Got response: {stdout[:200]}...")
            try:
                response_data = json.loads(stdout)
                print("✅ JSON parsed successfully!")
                return True
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                return False
        else:
            print("❌ No response from MCP server")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing MCP Server in Django-like Environment")
    print("=" * 60)
    
    success = test_mcp_in_django_env()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Test passed! MCP server communication works.")
    else:
        print("❌ Test failed. Check the output above for details.")
