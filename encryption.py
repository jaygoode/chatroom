from cryptography.fernet import Fernet

encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)


def encrypt_message(msg):
    msg_bytes = msg.encode()
    encrypted_msg = cipher_suite.encrypt(msg_bytes)
    return encrypt_message


def encrypt_message(msg):
    msg_bytes = msg.encode()
    encrypted_msg = cipher_suite.encrypt(msg_bytes)
    return encrypt_message
