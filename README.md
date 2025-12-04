# gRPC State Synchronization Experiment

This repository contains two simple Python applications that use gRPC to keep state in sync between a server and client.

## Overview

- **Server**: Maintains a simple key-value state and serves it to clients via gRPC
- **Client**: Can fetch state, update state, and watch for state changes in real-time

## Features

- Get current state from server
- Update state on server
- Real-time state change notifications (streaming)
- Interactive client mode
- Automated demo mode

## Setup

### Prerequisites

- Python 3.7 or higher
- pip

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

#### Interactive Mode

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

1. Start the server in terminal 1
2. Start client 1 in terminal 2 and run `watch` command
3. Start client 2 in terminal 3 and update state with `set` commands
4. Observe client 1 receiving real-time updates

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
- `src/client.py` - Client implementation

## State Model

The state is a simple dictionary mapping strings to integers:
- Keys: Any string
- Values: Integer values

This can be easily extended to support more complex data types by modifying the proto file.