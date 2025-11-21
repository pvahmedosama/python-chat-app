
import socket
import threading
import json

clients = {}         # {conn: {"name": str}}
usernames = {}       # {name: conn}

def send_json(conn, data):
    try:
        conn.send((json.dumps(data) + "\n").encode())
    except:
        pass

def broadcast(data, exclude=None):
    msg = (json.dumps(data) + "\n").encode()
    for c in list(clients.keys()):
        if c != exclude:
            try:
                c.send(msg)
            except:
                pass

def update_users():
    user_list = list(usernames.keys())
    broadcast({"type": "users", "users": user_list})

def handle_client(conn, addr):
    print(f"[NEW] {addr}")
    name = None
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            for line in data.splitlines():
                try:
                    msg = json.loads(line.decode())
                except:
                    continue
                mtype = msg.get("type")
                if mtype == "join":
                    name = msg["name"]
                    clients[conn] = {"name": name}
                    usernames[name] = conn
                    broadcast({"type": "info", "msg": f"{name} joined the chat"})
                    update_users()
                elif mtype == "msg":
                    broadcast({
                        "type": "msg",
                        "name": name,
                        "content": msg["content"]
                    })
                elif mtype == "pm":
                    to_user = msg["to"]
                    if to_user in usernames:
                        send_json(usernames[to_user], {
                            "type": "pm",
                            "from": name,
                            "content": msg["content"]
                        })
                    else:
                        send_json(conn, {"type": "error", "msg": "User not found"})
    except:
        pass
    finally:
        if name:
            print(f"[LEFT] {name}")
            broadcast({"type": "info", "msg": f"{name} left the chat"})
            if name in usernames:
                del usernames[name]
        if conn in clients:
            del clients[conn]
        update_users()
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 5000))
    server.listen()
    print("[SERVER] Running on port 5000...")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
