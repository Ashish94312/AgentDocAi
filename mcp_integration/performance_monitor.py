#!/usr/bin/env python3
"""
Performance monitoring script for CrewAI optimization
"""

import time
import psutil
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from mcp_manager.crews.crew import build_crew
from mcp_manager.crews.crew_async import build_crew_parallel
from mcp_manager.utils_optimized import cleanup_mcp_connections


class PerformanceMonitor:
    def __init__(self):
        self.start_time = None
        self.start_memory = None
        self.start_cpu = None
        
    def start_monitoring(self):
        """Start performance monitoring"""
        self.start_time = time.time()
        self.start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        self.start_cpu = psutil.cpu_percent()
        print(f"🚀 Starting performance monitoring...")
        print(f"📊 Initial Memory: {self.start_memory:.2f} MB")
        print(f"💻 Initial CPU: {self.start_cpu:.1f}%")
        
    def stop_monitoring(self):
        """Stop performance monitoring and print results"""
        if self.start_time is None:
            print("❌ Monitoring not started!")
            return
            
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        end_cpu = psutil.cpu_percent()
        
        execution_time = end_time - self.start_time
        memory_delta = end_memory - self.start_memory
        
        print(f"\n📈 Performance Results:")
        print(f"⏱️  Execution Time: {execution_time:.2f} seconds")
        print(f"🧠 Memory Usage: {end_memory:.2f} MB (Δ: {memory_delta:+.2f} MB)")
        print(f"💻 CPU Usage: {end_cpu:.1f}%")
        
        return {
            'execution_time': execution_time,
            'memory_usage': end_memory,
            'memory_delta': memory_delta,
            'cpu_usage': end_cpu
        }


def test_original_crew(owner, repo):
    """Test the original sequential crew"""
    print("\n🔄 Testing ORIGINAL Sequential Crew...")
    monitor = PerformanceMonitor()
    monitor.start_monitoring()
    
    try:
        crew = build_crew(owner, repo)
        crew.kickoff()
        cleanup_mcp_connections()
        return monitor.stop_monitoring()
    except Exception as e:
        print(f"❌ Error in original crew: {e}")
        return None


def test_optimized_crew(owner, repo):
    """Test the optimized parallel crew"""
    print("\n⚡ Testing OPTIMIZED Parallel Crew...")
    monitor = PerformanceMonitor()
    monitor.start_monitoring()
    
    try:
        results = build_crew_parallel(owner, repo)
        cleanup_mcp_connections()
        return monitor.stop_monitoring()
    except Exception as e:
        print(f"❌ Error in optimized crew: {e}")
        return None


def compare_performance(owner, repo):
    """Compare performance between original and optimized versions"""
    print(f"🔍 Performance Comparison for {owner}/{repo}")
    print("=" * 60)
    
    # Test original version
    original_results = test_original_crew(owner, repo)
    
    # Wait a bit between tests
    time.sleep(2)
    
    # Test optimized version
    optimized_results = test_optimized_crew(owner, repo)
    
    # Compare results
    if original_results and optimized_results:
        print("\n🏆 PERFORMANCE COMPARISON:")
        print("=" * 60)
        
        time_improvement = ((original_results['execution_time'] - optimized_results['execution_time']) / 
                          original_results['execution_time']) * 100
        
        memory_improvement = ((original_results['memory_usage'] - optimized_results['memory_usage']) / 
                            original_results['memory_usage']) * 100
        
        print(f"⏱️  Time Improvement: {time_improvement:+.1f}%")
        print(f"🧠 Memory Improvement: {memory_improvement:+.1f}%")
        
        if time_improvement > 0:
            print(f"✅ Optimized version is {time_improvement:.1f}% faster!")
        else:
            print(f"⚠️  Optimized version is {abs(time_improvement):.1f}% slower")
            
        print(f"\n📊 Detailed Results:")
        print(f"Original:  {original_results['execution_time']:.2f}s, {original_results['memory_usage']:.2f}MB")
        print(f"Optimized: {optimized_results['execution_time']:.2f}s, {optimized_results['memory_usage']:.2f}MB")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python performance_monitor.py <owner> <repo>")
        print("Example: python performance_monitor.py microsoft vscode")
        sys.exit(1)
    
    owner = sys.argv[1]
    repo = sys.argv[2]
    
    compare_performance(owner, repo)
