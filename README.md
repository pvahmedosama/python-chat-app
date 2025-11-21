
# Python Chat Application (Server + Client GUI)

This project is a simple chat application built with **Python Sockets** and a graphical user interface using **Tkinter**.  
It supports real-time communication with multiple clients connected to a central server.

---

## Features

- Public chat (Broadcast to all connected clients)
- Private messages using `/pm username message`
- Real-time online users list
- Join and Leave notifications
- TCP connection with JSON-based messaging

---

## Requirements

- Python 3.10 or higher
- No external libraries required (uses built-in `socket`, `threading`, `tkinter`, and `json`)

---

## Project Structure

```
Server.py     ← Server-side code
Client.py     ← Client GUI code using Tkinter
README.md     ← Project documentation
```

---

## Running the Server

Open a terminal and run:

```bash
python Server.py
```

You should see:

```
[SERVER] Running on port 5000...
```

---

## Running the Client

Open another terminal and run:

```bash
python Client.py
```

A window will prompt for your username.

---

## Sending Private Messages

Type the following in the message box:

```
/pm username Your message here
```

Or double-click a username in the online users list to prepare a private message automatically.

---

## Online Users List

The list updates automatically whenever a user joins or leaves the chat.

---

## JSON Message Structure

### Join

```json
{
  "type": "join",
  "name": "Ahmed"
}
```

### Public Message

```json
{
  "type": "msg",
  "content": "Hello everyone!"
}
```

### Private Message

```json
{
  "type": "pm",
  "to": "Ali",
  "content": "Hi bro"
}
```

---

## Notes

- Multiple clients can run on the same machine.
- Make sure the server is running before starting any client.
- The code is extendable to support:
  - File transfer
  - Chat rooms
  - End-to-End encryption

---

## License

This project is open and free to use without any restrictions.
