#!/usr/bin/env python3
"""
gRPC Client - Syncs state with server
"""

import grpc
import time
import sys
import os
import threading

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import statesync_pb2
import statesync_pb2_grpc


class StateClient:
    """Client that syncs state with server"""
    
    def __init__(self, server_address='localhost:50051'):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = statesync_pb2_grpc.StateSyncStub(self.channel)
        self.local_state = {}
        
    def get_state(self):
        """Fetch current state from server"""
        try:
            response = self.stub.GetState(statesync_pb2.Empty())
            self.local_state = dict(response.state)
            print(f"[Client] Fetched state from server: {self.local_state}")
            return self.local_state
        except grpc.RpcError as e:
            print(f"[Client] Error fetching state: {e}")
            return None
    
    def update_state(self, key, value):
        """Update state on server"""
        try:
            request = statesync_pb2.StateUpdate(key=key, value=value)
            response = self.stub.UpdateState(request)
            self.local_state = dict(response.state)
            print(f"[Client] Updated {key}={value}, server state: {self.local_state}")
            return self.local_state
        except grpc.RpcError as e:
            print(f"[Client] Error updating state: {e}")
            return None
    
    def watch_state(self):
        """Watch for state changes from server"""
        try:
            print("[Client] Watching for state changes...")
            for response in self.stub.WatchState(statesync_pb2.Empty()):
                self.local_state = dict(response.state)
                print(f"[Client] State changed: {self.local_state}")
        except grpc.RpcError as e:
            print(f"[Client] Watch ended: {e}")
    
    def close(self):
        """Close the channel"""
        self.channel.close()


def interactive_mode():
    """Run client in interactive mode"""
    client = StateClient()
    
    print("=== gRPC State Sync Client ===")
    print("Commands:")
    print("  get              - Get current state from server")
    print("  set <key> <val>  - Set a key-value pair")
    print("  watch            - Watch for state changes (Ctrl+C to stop)")
    print("  quit             - Exit")
    print()
    
    # Get initial state
    client.get_state()
    
    try:
        while True:
            try:
                cmd = input("\n> ").strip()
                
                if not cmd:
                    continue
                
                parts = cmd.split()
                command = parts[0].lower()
                
                if command == 'quit':
                    break
                elif command == 'get':
                    client.get_state()
                elif command == 'set':
                    if len(parts) != 3:
                        print("Usage: set <key> <value>")
                        continue
                    key = parts[1]
                    try:
                        value = int(parts[2])
                        client.update_state(key, value)
                    except ValueError:
                        print("Error: value must be an integer")
                elif command == 'watch':
                    print("Press Ctrl+C to stop watching")
                    try:
                        client.watch_state()
                    except KeyboardInterrupt:
                        print("\n[Client] Stopped watching")
                else:
                    print(f"Unknown command: {command}")
            except KeyboardInterrupt:
                print()
                continue
    finally:
        client.close()
        print("[Client] Disconnected")


def demo_mode():
    """Run automated demo"""
    client = StateClient()
    
    print("=== Running Demo Mode ===\n")
    
    # Get initial state
    print("1. Getting initial state...")
    client.get_state()
    time.sleep(1)
    
    # Update some values
    print("\n2. Setting counter=1...")
    client.update_state("counter", 1)
    time.sleep(1)
    
    print("\n3. Setting counter=5...")
    client.update_state("counter", 5)
    time.sleep(1)
    
    print("\n4. Setting score=100...")
    client.update_state("score", 100)
    time.sleep(1)
    
    print("\n5. Getting final state...")
    client.get_state()
    
    client.close()
    print("\n=== Demo Complete ===")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo_mode()
    else:
        interactive_mode()
