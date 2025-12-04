# gRPC State Synchronization Experiment

This repository contains two simple Python applications that use gRPC to keep state in sync between a server and client.

## Overview

- **Server**: Maintains a simple key-value state and serves it to clients via gRPC
- **Client (CLI)**: Command-line client that can fetch state, update state, and watch for state changes in real-time
- **Client (GUI)**: Tkinter-based GUI client that displays state and automatically updates when other clients change it

## Features

- Get current state from server
- Update state on server
- Real-time state change notifications (streaming)
- Interactive CLI client mode
- Automated demo mode
- **GUI client with automatic state synchronization**

## Setup

### Prerequisites

- Python 3.7 or higher
- pip
- Tkinter (for GUI client)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rishikhaneja/grpc_experiments.git
cd grpc_experiments
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

For the GUI client, also install Tkinter (if not already installed):
```bash
# On Ubuntu/Debian
sudo apt-get install python3-tk

# On macOS (usually pre-installed)
# On Windows (usually pre-installed with Python)
```

3. Generate gRPC code (already done, but if you modify the proto file):
```bash
python -m grpc_tools.protoc -I./proto --python_out=./src --grpc_python_out=./src ./proto/statesync.proto
```

## Usage

### Starting the Server

In one terminal, start the server:
```bash
python src/server.py
```

The server will start on port 50051 and wait for client connections.

### Running the Client

#### GUI Mode (Recommended)

Run the GUI client for a visual interface:
```bash
python src/client_gui.py
```

The GUI client features:
- Visual display of current state in a table
- Input fields to update state values
- Automatic real-time updates when other clients modify state
- Refresh button to manually fetch current state
- Status indicator showing connection and watch status

![GUI Client Empty State](https://github.com/user-attachments/assets/8ab906e5-0199-4e6d-a599-5b1cf4eb4a65)

![GUI Client With State](https://github.com/user-attachments/assets/c2e8aa6e-2a6d-4c94-abd6-c2a6d26b6cb9)

#### Interactive Mode (CLI)

In another terminal, run the client in interactive mode:
```bash
python src/client.py
```

Available commands:
- `get` - Fetch current state from server
- `set <key> <value>` - Update a key-value pair (value must be an integer)
- `watch` - Subscribe to real-time state changes (Ctrl+C to stop watching)
- `quit` - Exit the client

Example session:
```
> get
[Client] Fetched state from server: {}

> set counter 1
[Client] Updated counter=1, server state: {'counter': 1}

> set counter 5
[Client] Updated counter=5, server state: {'counter': 5}

> set score 100
[Client] Updated score=100, server state: {'counter': 5, 'score': 100}

> get
[Client] Fetched state from server: {'counter': 5, 'score': 100}
```

#### Demo Mode

Run the client in automated demo mode:
```bash
python src/client.py --demo
```

This will automatically demonstrate the state synchronization features.

### Testing with Multiple Clients

You can run multiple clients simultaneously to see state synchronization in action:

**Option 1: Multiple GUI clients**
1. Start the server in terminal 1
2. Start GUI client 1 in terminal 2: `python src/client_gui.py`
3. Start GUI client 2 in terminal 3: `python src/client_gui.py`
4. Update state in GUI client 1 and watch it automatically appear in GUI client 2

**Option 2: Mixed CLI and GUI clients**
1. Start the server in terminal 1
2. Start GUI client in terminal 2: `python src/client_gui.py`
3. Start CLI client in terminal 3 and run `set counter 42`
4. Observe the GUI automatically updating with the new state

## Architecture

### Protocol Buffer Definition

The gRPC service is defined in `proto/statesync.proto`:

- **GetState**: Fetch current state snapshot
- **UpdateState**: Update a key-value pair
- **WatchState**: Subscribe to state changes (server streaming)

### Components

- `proto/statesync.proto` - Protocol buffer definition
- `src/statesync_pb2.py` - Generated protobuf messages
- `src/statesync_pb2_grpc.py` - Generated gRPC service stubs
- `src/server.py` - Server implementation
- `src/client.py` - CLI client implementation
- `src/client_gui.py` - GUI client implementation (Tkinter)

## State Model

The state is a simple dictionary mapping strings to integers:
- Keys: Any string
- Values: Integer values

This can be easily extended to support more complex data types by modifying the proto file.