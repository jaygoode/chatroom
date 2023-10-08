from cryptography.fernet import Fernet
import socket

# Assuming you have the encryption key stored in `encryption_key`
encryption_key = b'QHwEvyLkqhtl4KbXftzn9Sd1-1ONoT4cx9Qb8tGsf6k='
cipher_suite = Fernet(encryption_key)

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
# Change this to the desired address and port
server_address = ('localhost', 12345)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print("Waiting for a connection...")
connection, client_address = server_socket.accept()

try:
    # Receive the encrypted message
    encrypted_msg = connection.recv(2048)

    # Decrypt the message
    decrypted_msg = cipher_suite.decrypt(encrypted_msg).decode()

    print(f"Received encrypted message: {encrypted_msg}")
    print(f"Decrypted message: {decrypted_msg}")

finally:
    # Clean up the connection
    connection.close()

# Close the server socket
server_socket.close()
