from app import app
import os, socket

if __name__ == "__main__":
    print(socket.gethostbyname(socket.gethostname()))
    app.run()