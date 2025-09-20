import socket
import threading
import json
import time

PEERS_FILE = "peers.json"
PEERS = set()

def save_peers(peers):
    with open(PEERS_FILE, "w") as f:
        json.dump(list(peers), f)

def load_peers():
    try:
        with open(PEERS_FILE, "r") as f:
            return set(tuple(p) for p in json.load(f))
    except Exception:
        return set()

PEERS = load_peers()

def start_server(host, port, handle_message):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Node listening on {host}:{port}")

    def client_thread(conn, addr):
        while True:
            data = conn.recv(4096)
            if not data:
                break
            try:
                msg = json.loads(data.decode())
                handle_message(msg, addr)
            except Exception as e:
                print(f"Error processing message: {e}")
        conn.close()

    def accept_connections():
        while True:
            conn, addr = server.accept()
            threading.Thread(target=client_thread, args=(conn, addr)).start()

    threading.Thread(target=accept_connections, daemon=True).start()

def connect_to_peer(host, port):
    peer = (host, port)
    PEERS.add(peer)
    save_peers(PEERS)
    print(f"Connected to peer {peer}")

def broadcast_message(message):
    msg_str = json.dumps(message)
    for peer in PEERS:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(peer)
            s.sendall(msg_str.encode())
            s.close()
        except Exception as e:
            print(f"Could not send to {peer}: {e}")

def request_chain_from_peer(peer):
    """Request the full chain from a peer."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(peer)
        s.sendall(json.dumps({"type": "get_chain"}).encode())
        s.close()
    except Exception as e:
        print(f"Could not request chain from {peer}: {e}"