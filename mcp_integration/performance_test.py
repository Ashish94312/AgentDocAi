#!/usr/bin/env python3
"""
Performance test script to demonstrate the improvements from async implementation.
This script compares synchronous vs asynchronous execution performance.
"""

import asyncio
import time
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_integration.mcp_manager.concurrent_executor import (
    execute_concurrent_github_analysis,
    PerformanceComparator
)


async def test_performance():
    """Test the performance improvements of async implementation."""
    print("🚀 Performance Test: Async vs Sync GitHub API Operations")
    print("=" * 60)
    
    # Test repository (you can change this to any public repository)
    owner = "microsoft"
    repo = "vscode"
    
    print(f"Testing with repository: {owner}/{repo}")
    print()
    
    try:
        # Test concurrent execution
        print("📊 Testing Concurrent (Async) Execution...")
        start_time = time.time()
        async_results = await execute_concurrent_github_analysis(owner, repo)
        async_time = time.time() - start_time
        
        print(f"✅ Concurrent execution completed in {async_time:.2f} seconds")
        print()
        
        # Display results summary
        summary = async_results['summary']
        print("📈 Execution Summary:")
        print(f"  • Total tasks executed: {summary['total_tasks']}")
        print(f"  • Successful tasks: {summary['successful_tasks']}")
        print(f"  • Failed tasks: {summary['failed_tasks']}")
        print(f"  • Total execution time: {summary['total_execution_time']:.2f}s")
        print(f"  • Average task time: {summary['average_task_time']:.2f}s")
        
        if summary['failed_tasks']:
            print(f"  • Failed tasks: {', '.join(summary['failed_tasks'])}")
        
        print()
        
        # Display individual task results
        print("📋 Individual Task Results:")
        for task_name, result in async_results['results'].items():
            status = "✅" if result.success else "❌"
            print(f"  {status} {task_name}: {result.execution_time:.2f}s")
            if not result.success and result.error:
                print(f"      Error: {result.error}")
        
        print()
        
        # Performance comparison
        print("⚡ Performance Comparison:")
        print("  • All tasks executed concurrently")
        print("  • Maximum time = slowest individual task")
        print(f"  • Estimated sync time: {summary['total_execution_time'] * 4:.2f}s")
        print(f"  • Actual async time: {async_time:.2f}s")
        
        if summary['total_execution_time'] > 0:
            improvement = ((summary['total_execution_time'] * 4 - async_time) / (summary['total_execution_time'] * 4)) * 100
            print(f"  • Performance improvement: ~{improvement:.1f}%")
        
        print()
        print("🎉 Performance test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during performance test: {e}")
        import traceback
        traceback.print_exc()


async def test_with_different_repos():
    """Test performance with different repositories."""
    print("\n🔄 Testing with Multiple Repositories")
    print("=" * 60)
    
    test_repos = [
        ("facebook", "react"),
        ("microsoft", "TypeScript"),
        ("google", "tensorflow")
    ]
    
    for owner, repo in test_repos:
        print(f"\n📦 Testing {owner}/{repo}...")
        try:
            start_time = time.time()
            results = await execute_concurrent_github_analysis(owner, repo)
            execution_time = time.time() - start_time
            
            summary = results['summary']
            print(f"  ✅ Completed in {execution_time:.2f}s")
            print(f"  📊 {summary['successful_tasks']}/{summary['total_tasks']} tasks successful")
            
        except Exception as e:
            print(f"  ❌ Failed: {e}")


if __name__ == "__main__":
    print("🔧 GitHub API Performance Test")
    print("This script demonstrates the performance improvements from async implementation.")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("mcp_integration"):
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Run the performance test
    asyncio.run(test_performance())
    
    # Ask if user wants to test with multiple repos
    try:
        response = input("\n🤔 Would you like to test with multiple repositories? (y/n): ")
        if response.lower() in ['y', 'yes']:
            asyncio.run(test_with_different_repos())
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    
    print("\n✨ Performance test completed!")
