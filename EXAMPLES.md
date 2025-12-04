# Example Usage

This document demonstrates how to use the gRPC state synchronization applications.

## Quick Start

### Terminal 1: Start the Server
```bash
python src/server.py
```

Output:
```
[Server] Started on port 50051
[Server] Waiting for clients...
```

### Terminal 2: Run Client Demo
```bash
python src/client.py --demo
```

Output:
```
=== Running Demo Mode ===

1. Getting initial state...
[Client] Fetched state from server: {}

2. Setting counter=1...
[Client] Updated counter=1, server state: {'counter': 1}

3. Setting counter=5...
[Client] Updated counter=5, server state: {'counter': 5}

4. Setting score=100...
[Client] Updated score=100, server state: {'score': 100, 'counter': 5}

5. Getting final state...
[Client] Fetched state from server: {'score': 100, 'counter': 5}

=== Demo Complete ===
```

## Interactive Client Example

### Terminal 2: Start Interactive Client
```bash
python src/client.py
```

Then type commands:
```
> set players 4
[Client] Updated players=4, server state: {'players': 4}

> set level 10
[Client] Updated level=10, server state: {'players': 4, 'level': 10}

> get
[Client] Fetched state from server: {'players': 4, 'level': 10}

> quit
[Client] Disconnected
```

## Multi-Client Demo

### Terminal 1: Server
```bash
python src/server.py
```

### Terminal 2: Client watching for changes
```bash
python src/client.py
```
Then type: `watch`

### Terminal 3: Client making updates
```bash
python src/client.py
```
Then type commands like: `set counter 1`, `set counter 2`, etc.

You'll see Terminal 2 automatically display all the state changes in real-time!
