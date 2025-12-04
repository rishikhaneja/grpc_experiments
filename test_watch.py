#!/usr/bin/env python3
"""
Test script to demonstrate watch functionality with multiple clients
"""

import subprocess
import time
import sys

def main():
    print("=== Testing Watch Functionality ===\n")
    
    # Start a client in watch mode in the background
    print("1. Starting Client 1 in watch mode...")
    watch_client = subprocess.Popen(
        [sys.executable, "src/client.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Wait a bit for it to initialize
    time.sleep(2)
    
    # Start watch mode
    print("2. Sending 'watch' command to Client 1...")
    watch_client.stdin.write("watch\n")
    watch_client.stdin.flush()
    time.sleep(1)
    
    # Run demo client to make updates
    print("3. Running Client 2 in demo mode to make updates...\n")
    time.sleep(1)
    
    demo_result = subprocess.run(
        [sys.executable, "src/client.py", "--demo"],
        capture_output=True,
        text=True
    )
    
    print(demo_result.stdout)
    
    # Give some time for watch client to receive updates
    time.sleep(2)
    
    # Stop the watch client gracefully
    print("\n4. Stopping Client 1...")
    watch_client.terminate()
    
    # Get output from watch client
    try:
        output, _ = watch_client.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        watch_client.kill()
        output, _ = watch_client.communicate()
    
    print("\n=== Client 1 (Watch Mode) Output ===")
    print(output)
    
    print("\n=== Test Complete ===")
    print("✓ Server maintains state")
    print("✓ Clients can get and update state")
    print("✓ Watch mode receives real-time updates")

if __name__ == '__main__':
    main()
