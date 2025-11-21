# client_gui.py
import socket
import threading
import json
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QListWidget,
    QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt


class Client:
    def __init__(self, gui):
        self.gui = gui
        self.sock = socket.socket()
        self.connected = False

    def connect(self, name):
        try:
            self.sock.connect(("127.0.0.1", 5000))
            self.connected = True
            self.send_json({"type": "join", "name": name})
            threading.Thread(target=self.listen, daemon=True).start()
            return True
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to connect: {e}")
            return False

    def listen(self):
        while True:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                for line in data.splitlines():
                    try:
                        msg = json.loads(line.decode())
                        self.gui.handle_message(msg)
                    except:
                        continue
            except:
                break

    def send_json(self, data):
        try:
            self.sock.send((json.dumps(data) + "\n").encode())
        except:
            pass

    def send_message(self, msg):
        if msg.startswith("/pm"):
            parts = msg.split()
            if len(parts) >= 3:
                _, user, *content = parts
                content = " ".join(content)
                self.send_json({"type": "pm", "to": user, "content": content})
        else:
            self.send_json({"type": "msg", "content": msg})


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Client (PyQt6)")
        self.resize(700, 500)

        # Layouts
        main_layout = QHBoxLayout(self)
        self.users_list = QListWidget()
        self.users_list.setFixedWidth(200)
        main_layout.addWidget(self.users_list)

        chat_layout = QVBoxLayout()
        main_layout.addLayout(chat_layout)

        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)
        chat_layout.addWidget(self.chat_view)

        bottom_layout = QHBoxLayout()
        self.input_line = QLineEdit()
        bottom_layout.addWidget(self.input_line)
        send_btn = QPushButton("Send")
        bottom_layout.addWidget(send_btn)
        chat_layout.addLayout(bottom_layout)

        # Signals
        send_btn.clicked.connect(self.send_message)
        self.input_line.returnPressed.connect(self.send_message)
        self.users_list.itemDoubleClicked.connect(self.on_user_double)

        # Client initiator
        self.client = Client(self)
        self.ask_name()

    def ask_name(self):
        name, ok = QInputDialog.getText(self, "Login", "Enter your name:")
        if ok and name:
            if not self.client.connect(name):
                self.close()
        else:
            self.close()

    def send_message(self):
        text = self.input_line.text().strip()
        if text:
            self.client.send_message(text)
            self.input_line.clear()

    def handle_message(self, msg):
        mtype = msg.get("type")
        if mtype == "msg":
            self.write(f"{msg.get('name')}: {msg.get('content')}")
        elif mtype == "info":
            self.write(f"[INFO] {msg.get('msg')}", color="blue")
        elif mtype == "pm":
            self.write(f"[PRIVATE] {msg.get('from')}: {msg.get('content')}", color="purple")
        elif mtype == "users":
            self.users_list.clear()
            for u in msg.get("users", []):
                self.users_list.addItem(u)

    def write(self, text, color="black"):
        self.chat_view.setTextColor(
            Qt.GlobalColor.black if color=="black" else
            (Qt.GlobalColor.blue if color=="blue" else Qt.GlobalColor.magenta)
        )
        self.chat_view.append(text)

    def on_user_double(self, item):
        user = item.text()
        self.input_line.setText(f"/pm {user} ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())
