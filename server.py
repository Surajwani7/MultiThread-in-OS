import socket
import threading
import wikipedia

# Constants
IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

# Function to handle client connections
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False

        print(f"[{addr}] {msg}")
        # Retrieve a Wikipedia summary for the received message
        try:
            summary = wikipedia.summary(msg, sentences=1)
            conn.send(summary.encode(FORMAT))
        except wikipedia.exceptions.DisambiguationError as e:
            conn.send("Ambiguous query. Please provide more specific input.".encode(FORMAT))
        except wikipedia.exceptions.PageError as e:
            conn.send("No matching results found on Wikipedia.".encode(FORMAT))

    conn.close()

# Main function to start the server
def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()
