import socket
from cryptography.fernet import Fernet

# Assuming you have the encryption key stored in `encryption_key`
encryption_key = b'QHwEvyLkqhtl4KbXftzn9Sd1-1ONoT4cx9Qb8tGsf6k='
cipher_suite = Fernet(encryption_key)

# Message to encrypt and send
message = "Hello, this is a test message."

# Encrypt the message
encrypted_msg = cipher_suite.encrypt(message.encode())

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 12345)  # Change this to the server's address
client_socket.connect(server_address)

# Send the encrypted message
client_socket.sendall(encrypted_msg)

# Close the client socket
client_socket.close()
