# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Server (port 50051)                  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  StateSyncServicer                                     │ │
│  │                                                         │ │
│  │  State: { "counter": 5, "score": 100 }                 │ │
│  │                                                         │ │
│  │  Methods:                                               │ │
│  │  • GetState()        → Returns current state           │ │
│  │  • UpdateState()     → Updates state & notifies        │ │
│  │  • WatchState()      → Streams state changes           │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────▲───────────────────────────▲──────────────────┘
               │                           │
               │  gRPC calls               │  gRPC calls
               │                           │
      ┌────────┴─────────┐        ┌───────┴──────────┐
      │   Client 1       │        │    Client 2      │
      │                  │        │                  │
      │  Interactive     │        │  Demo Mode       │
      │  Mode:           │        │                  │
      │  • get           │        │  Automated       │
      │  • set key val   │        │  operations      │
      │  • watch         │        │                  │
      │  • quit          │        │                  │
      └──────────────────┘        └──────────────────┘
```

## Communication Flow

### 1. Get State
```
Client ──GetState()──> Server
Client <──StateResponse── Server
```

### 2. Update State
```
Client ──UpdateState(key, value)──> Server
                                     Server updates state
                                     Server notifies watchers
Client <──StateResponse────────────── Server
```

### 3. Watch State (Streaming)
```
Client ──WatchState()──> Server
Client <──StateResponse── Server (initial state)
Client <──StateResponse── Server (when state changes)
Client <──StateResponse── Server (when state changes)
...
```

## State Model

```
State = Dictionary<String, Integer>

Examples:
  { "counter": 42 }
  { "counter": 5, "score": 100, "level": 3 }
  { "players": 4, "round": 2 }
```

## Protocol Buffer Definition

```protobuf
service StateSync {
  rpc GetState(Empty) returns (StateResponse);
  rpc UpdateState(StateUpdate) returns (StateResponse);
  rpc WatchState(Empty) returns (stream StateResponse);
}

message StateUpdate {
  string key = 1;
  int32 value = 2;
}

message StateResponse {
  map<string, int32> state = 1;
}
```

## Use Cases

### Use Case 1: Periodic State Check
```
Client periodically calls GetState() to sync with server
```

### Use Case 2: State Updates
```
Client modifies state by calling UpdateState()
Server broadcasts changes to all watching clients
```

### Use Case 3: Real-time Monitoring
```
Client calls WatchState() to establish streaming connection
Client receives all future state updates automatically
```
