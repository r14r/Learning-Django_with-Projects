# Specification: Real-Time Chat Application

**Level:** Advanced  
**Project:** 04_chat_app  
**Description:** WebSocket-based real-time chat using Django Channels

---

## 1. Overview

Build a multi-room real-time chat application using Django Channels and WebSockets.
Users can create and join rooms, send messages that appear instantly for all participants,
and see an online-users indicator.

## 2. Goals

- Set up Django Channels with an ASGI server (Daphne / Uvicorn)
- Implement a WebSocket consumer that broadcasts messages to a channel group
- Store chat rooms and message history in the database
- Serve the chat UI with HTMX or vanilla JavaScript WebSocket API

## 3. Functional Requirements

| # | Feature | Priority |
|---|---------|----------|
| 1 | List of chat rooms | Must |
| 2 | Create a new room | Must |
| 3 | Join a room and receive real-time messages | Must |
| 4 | Send a message that all room members see | Must |
| 5 | Persist messages in the database | Must |
| 6 | Display last 50 messages on join | Should |
| 7 | Show online user count | Should |
| 8 | Private (direct) messages | Could |

## 4. Data Model

```
Room
├── id      : AutoField
├── name    : CharField(max_length=100, unique=True)
├── slug    : SlugField(unique=True)
└── created_at : DateTimeField(auto_now_add=True)

Message
├── id         : AutoField
├── room       : ForeignKey(Room, related_name='messages')
├── author     : ForeignKey(User)
├── content    : TextField
└── timestamp  : DateTimeField(auto_now_add=True)
```

## 5. URL Structure

| URL | View | Name |
|-----|------|------|
| `/` | RoomListView | `chat:list` |
| `/room/<slug>/` | room_view | `chat:room` |
| `/ws/chat/<slug>/` | ChatConsumer (WebSocket) | — |

## 6. Acceptance Criteria

- [ ] WebSocket connection established on room page
- [ ] Messages broadcast to all connected clients in the room
- [ ] Messages persisted and shown on reconnect (last 50)
- [ ] Login required to join a room
- [ ] At least 8 tests pass (sync HTTP tests + async consumer tests)

## 7. Out of Scope

- End-to-end encryption
- File attachments in chat
