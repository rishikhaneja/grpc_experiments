#!/usr/bin/env python3
"""
gRPC Server - Maintains and serves state to clients
"""

import grpc
from concurrent import futures
import time
import threading
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import statesync_pb2
import statesync_pb2_grpc


class StateSyncServicer(statesync_pb2_grpc.StateSyncServicer):
    """Implementation of StateSync service"""
    
    def __init__(self):
        # Simple state: a dictionary of key-value pairs
        self.state = {}
        self.lock = threading.Lock()
        self.observers = []
        
    def GetState(self, request, context):
        """Return current state"""
        with self.lock:
            print(f"[Server] Client requested state: {dict(self.state)}")
            return statesync_pb2.StateResponse(state=self.state)
    
    def UpdateState(self, request, context):
        """Update state and notify observers"""
        with self.lock:
            old_value = self.state.get(request.key, None)
            self.state[request.key] = request.value
            print(f"[Server] State updated: {request.key}={request.value} (was {old_value})")
            print(f"[Server] Current state: {dict(self.state)}")
            
            # Notify all watching clients
            response = statesync_pb2.StateResponse(state=self.state)
            for observer in self.observers:
                try:
                    observer.put(response)
                except:
                    pass
            
            return response
    
    def WatchState(self, request, context):
        """Stream state changes to client"""
        import queue
        q = queue.Queue()
        self.observers.append(q)
        
        print("[Server] Client subscribed to state changes")
        
        try:
            # Send initial state
            with self.lock:
                yield statesync_pb2.StateResponse(state=self.state)
            
            # Stream updates
            while context.is_active():
                try:
                    response = q.get(timeout=1.0)
                    yield response
                except queue.Empty:
                    continue
        finally:
            self.observers.remove(q)
            print("[Server] Client unsubscribed from state changes")


def serve():
    """Start the gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    statesync_pb2_grpc.add_StateSyncServicer_to_server(
        StateSyncServicer(), server
    )
    
    port = '50051'
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print(f"[Server] Started on port {port}")
    print("[Server] Waiting for clients...")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[Server] Shutting down...")
        server.stop(0)


if __name__ == '__main__':
    serve()
