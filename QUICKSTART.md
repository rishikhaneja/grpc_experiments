# Quick Reference Guide

## Setup (One-time)

```bash
# Install dependencies
pip install -r requirements.txt

# Regenerate gRPC code (only if you modify the .proto file)
python -m grpc_tools.protoc -I./proto --python_out=./src --grpc_python_out=./src ./proto/statesync.proto
```

## Running the Applications

### Start Server
```bash
python src/server.py
# Output: [Server] Started on port 50051
```

### Run Client (Interactive)
```bash
python src/client.py
# Then use commands: get, set <key> <value>, watch, quit
```

### Run Client (Demo Mode)
```bash
python src/client.py --demo
# Runs automated demonstration
```

## Common Operations

### Get current state
```python
> get
[Client] Fetched state from server: {'counter': 5}
```

### Set a value
```python
> set counter 10
[Client] Updated counter=10, server state: {'counter': 10}
```

### Watch for changes
```python
> watch
[Client] Watching for state changes...
# (Updates appear automatically when other clients modify state)
# Press Ctrl+C to stop
```

## Testing

### Test Watch Functionality
```bash
python test_watch.py
```

### Manual Multi-Client Test
1. Terminal 1: `python src/server.py`
2. Terminal 2: `python src/client.py` then type `watch`
3. Terminal 3: `python src/client.py` then type `set counter 1`, `set counter 2`, etc.
4. Observe Terminal 2 receiving updates in real-time

## Project Structure

```
grpc_experiments/
├── proto/
│   └── statesync.proto          # gRPC service definition
├── src/
│   ├── server.py                # Server application
│   ├── client.py                # Client application
│   ├── statesync_pb2.py         # Generated protobuf (auto-generated)
│   └── statesync_pb2_grpc.py    # Generated gRPC stubs (auto-generated)
├── requirements.txt              # Python dependencies
├── test_watch.py                # Test script
├── README.md                    # Main documentation
├── EXAMPLES.md                  # Usage examples
├── ARCHITECTURE.md              # Architecture overview
└── QUICKSTART.md                # This file
```

## Troubleshooting

### Server won't start
- Check if port 50051 is already in use
- Try: `lsof -i :50051` to see what's using the port
- Kill existing process or change the port in server.py

### Client can't connect
- Ensure server is running
- Check server address (default: localhost:50051)
- Verify firewall settings

### Proto file changes not reflected
- Regenerate code with: `python -m grpc_tools.protoc -I./proto --python_out=./src --grpc_python_out=./src ./proto/statesync.proto`
- Restart server and clients

## Key Concepts

- **State**: Dictionary mapping string keys to integer values
- **GetState**: One-time state fetch
- **UpdateState**: Modify state and notify watchers
- **WatchState**: Continuous stream of state updates
- **Observers**: Clients watching for state changes
