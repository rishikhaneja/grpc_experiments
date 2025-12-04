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

### Terminal 2: Run GUI Client
```bash
python src/client_gui.py
```

The GUI client will:
- Automatically connect to the server
- Display the current state in a table
- Start watching for state changes
- Allow you to update state through input fields

### Terminal 3: Run CLI Client Demo
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

Watch the GUI client automatically update as the CLI demo runs!

## GUI Client Example

### Using the GUI to Update State

1. Start the server: `python src/server.py`
2. Start the GUI client: `python src/client_gui.py`
3. In the GUI:
   - Enter "counter" in the Key field
   - Enter "42" in the Value field
   - Click "Update State"
   - See the state table automatically update

### Watching State Sync Between GUI Clients

1. Start the server in terminal 1
2. Start GUI client #1 in terminal 2
3. Start GUI client #2 in terminal 3
4. Update state in GUI client #1
5. Watch GUI client #2 automatically update in real-time!

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

### Option 1: Multiple GUI Clients

**Terminal 1: Server**
```bash
python src/server.py
```

**Terminal 2: GUI Client 1**
```bash
python src/client_gui.py
```

**Terminal 3: GUI Client 2**
```bash
python src/client_gui.py
```

Now update state in either GUI and watch both update automatically!

### Option 2: CLI + GUI Mixed Demo

**Terminal 1: Server**
```bash
python src/server.py
```

**Terminal 2: GUI Client (watching)**
```bash
python src/client_gui.py
```

**Terminal 3: CLI Client (making updates)**
```bash
python src/client.py
```
Then type commands like: `set counter 1`, `set counter 2`, etc.

You'll see the GUI automatically display all the state changes in real-time!
