#!/usr/bin/env python3
"""
gRPC Client with Tkinter GUI - Displays and syncs state with server
"""

import grpc
import sys
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import statesync_pb2
import statesync_pb2_grpc


class StateClientGUI:
    """GUI Client that syncs state with server"""
    
    def __init__(self, root, server_address='localhost:50051'):
        self.root = root
        self.root.title("gRPC State Sync Client")
        self.root.geometry("600x500")
        
        # gRPC connection
        self.channel = grpc.insecure_channel(server_address)
        self.stub = statesync_pb2_grpc.StateSyncStub(self.channel)
        self.local_state = {}
        self.watch_thread = None
        self.watching = False
        
        # Create GUI elements
        self.create_widgets()
        
        # Fetch initial state and start watching
        self.get_state()
        self.start_watching()
    
    def create_widgets(self):
        """Create GUI widgets"""
        # Title
        title_label = tk.Label(
            self.root,
            text="gRPC State Synchronization",
            font=("Arial", 16, "bold"),
            bg="#2196F3",
            fg="white",
            pady=10
        )
        title_label.pack(fill=tk.X)
        
        # State display frame
        state_frame = tk.LabelFrame(
            self.root,
            text="Current State",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        state_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for displaying state
        columns = ("Key", "Value")
        self.state_tree = ttk.Treeview(
            state_frame,
            columns=columns,
            show="headings",
            height=10
        )
        self.state_tree.heading("Key", text="Key")
        self.state_tree.heading("Value", text="Value")
        self.state_tree.column("Key", width=250)
        self.state_tree.column("Value", width=250)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(
            state_frame,
            orient=tk.VERTICAL,
            command=self.state_tree.yview
        )
        self.state_tree.configure(yscroll=scrollbar.set)
        
        self.state_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Update frame
        update_frame = tk.LabelFrame(
            self.root,
            text="Update State",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        update_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Key input
        tk.Label(update_frame, text="Key:", font=("Arial", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.key_entry = tk.Entry(update_frame, font=("Arial", 10), width=20)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Value input
        tk.Label(update_frame, text="Value:", font=("Arial", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.value_entry = tk.Entry(update_frame, font=("Arial", 10), width=20)
        self.value_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Update button
        update_btn = tk.Button(
            update_frame,
            text="Update State",
            command=self.on_update_click,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        )
        update_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Status: Connected and watching for changes...",
            font=("Arial", 9),
            bg="#f0f0f0",
            anchor=tk.W,
            padx=10,
            pady=5
        )
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Refresh button
        refresh_frame = tk.Frame(self.root)
        refresh_frame.pack(fill=tk.X, padx=10, pady=5)
        
        refresh_btn = tk.Button(
            refresh_frame,
            text="Refresh State",
            command=self.get_state,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            padx=10,
            pady=5
        )
        refresh_btn.pack(side=tk.LEFT)
        
        # Watch status indicator
        self.watch_indicator = tk.Label(
            refresh_frame,
            text="● Watching",
            font=("Arial", 10),
            fg="green"
        )
        self.watch_indicator.pack(side=tk.RIGHT, padx=10)
    
    def update_state_display(self):
        """Update the treeview with current state"""
        # Clear existing items
        for item in self.state_tree.get_children():
            self.state_tree.delete(item)
        
        # Add current state items
        for key, value in sorted(self.local_state.items()):
            self.state_tree.insert("", tk.END, values=(key, value))
        
        # Update status
        self.status_label.config(
            text=f"Status: State updated - {len(self.local_state)} items"
        )
    
    def get_state(self):
        """Fetch current state from server"""
        try:
            response = self.stub.GetState(statesync_pb2.Empty())
            self.local_state = dict(response.state)
            self.update_state_display()
            print(f"[GUI Client] Fetched state from server: {self.local_state}")
        except grpc.RpcError as e:
            self.status_label.config(text=f"Status: Error fetching state - {e}")
            print(f"[GUI Client] Error fetching state: {e}")
    
    def update_state(self, key, value):
        """Update state on server"""
        try:
            request = statesync_pb2.StateUpdate(key=key, value=value)
            response = self.stub.UpdateState(request)
            self.local_state = dict(response.state)
            self.update_state_display()
            print(f"[GUI Client] Updated {key}={value}, server state: {self.local_state}")
        except grpc.RpcError as e:
            self.status_label.config(text=f"Status: Error updating state - {e}")
            print(f"[GUI Client] Error updating state: {e}")
    
    def on_update_click(self):
        """Handle update button click"""
        key = self.key_entry.get().strip()
        value_str = self.value_entry.get().strip()
        
        if not key:
            messagebox.showerror("Error", "Key cannot be empty")
            return
        
        if not value_str:
            messagebox.showerror("Error", "Value cannot be empty")
            return
        
        try:
            value = int(value_str)
            self.update_state(key, value)
            # Clear inputs after successful update
            self.key_entry.delete(0, tk.END)
            self.value_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Value must be an integer")
    
    def watch_state(self):
        """Watch for state changes from server (runs in separate thread)"""
        try:
            print("[GUI Client] Started watching for state changes...")
            for response in self.stub.WatchState(statesync_pb2.Empty()):
                if not self.watching:
                    break
                self.local_state = dict(response.state)
                # Schedule UI update on main thread
                self.root.after(0, self.update_state_display)
                print(f"[GUI Client] State changed: {self.local_state}")
        except grpc.RpcError as e:
            error_msg = str(e)
            print(f"[GUI Client] Watch ended: {error_msg}")
            if self.watching:
                self.root.after(0, lambda msg=error_msg: self.status_label.config(
                    text=f"Status: Watch ended - {msg}"
                ))
    
    def start_watching(self):
        """Start watching for state changes in a separate thread"""
        # Only start if not already watching
        if self.watch_thread is not None and self.watch_thread.is_alive():
            return
        
        self.watching = True
        self.watch_thread = threading.Thread(target=self.watch_state, daemon=True)
        self.watch_thread.start()
    
    def stop_watching(self):
        """Stop watching for state changes"""
        self.watching = False
        self.watch_indicator.config(text="● Not Watching", fg="red")
    
    def close(self):
        """Close the channel and stop watching"""
        self.stop_watching()
        self.channel.close()
        print("[GUI Client] Disconnected")


def main():
    """Main function to run the GUI client"""
    root = tk.Tk()
    
    # Create the GUI client
    client = StateClientGUI(root)
    
    # Handle window close
    def on_closing():
        client.close()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == '__main__':
    main()
