#!/usr/bin/env python3
"""
Direct test of MCP server communication
"""
import json
import subprocess
import os
import sys

def test_mcp_server():
    # Set the GitHub token
    os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'] = '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'
    
    # Path to the MCP server
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mcp_server_path = os.path.join(project_root, 'github-mcp-server', 'github-mcp-server')
    
    # Test 1: List tools
    print("=== Testing MCP Server Tools List ===")
    tools_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }
    
    try:
        process = subprocess.Popen(
            [mcp_server_path, '--toolsets', 'repos,issues,pull_requests,code_security', 'stdio'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=os.environ,
            text=True
        )
        
        stdout, stderr = process.communicate(input=json.dumps(tools_request) + '\n', timeout=30)
        
        if stderr:
            print(f"Stderr: {stderr}")
        
        if stdout:
            print(f"Response: {stdout}")
            try:
                response = json.loads(stdout)
                print("✅ Tools list successful!")
                return True
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                return False
        else:
            print("❌ No response from server")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_file_contents():
    # Set the GitHub token
    os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'] = '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'
    
    # Path to the MCP server
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mcp_server_path = os.path.join(project_root, 'github-mcp-server', 'github-mcp-server')
    
    # Test 2: Get file contents
    print("\n=== Testing Get File Contents ===")
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
    
    try:
        process = subprocess.Popen(
            [mcp_server_path, '--toolsets', 'repos,issues,pull_requests,code_security', 'stdio'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=os.environ,
            text=True
        )
        
        stdout, stderr = process.communicate(input=json.dumps(file_request) + '\n', timeout=30)
        
        if stderr:
            print(f"Stderr: {stderr}")
        
        if stdout:
            print(f"Response: {stdout}")
            try:
                response = json.loads(stdout)
                print("✅ Get file contents successful!")
                return True
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                return False
        else:
            print("❌ No response from server")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing MCP Server Direct Communication")
    print("=" * 50)
    
    # Test tools list
    tools_success = test_mcp_server()
    
    # Test get file contents
    file_success = test_get_file_contents()
    
    print("\n" + "=" * 50)
    if tools_success and file_success:
        print("✅ All tests passed! MCP server is working correctly.")
    else:
        print("❌ Some tests failed. Check the output above for details.")
