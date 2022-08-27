# main.py
import os
import socket
import pyautogui
import qrcode
import base64
import aes_cipher
import _thread as thread
from PIL import Image

secret_key = bytearray(os.urandom(32))


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


ip = get_local_ip()


def build_connection_params(s):
    s.bind((ip, 0))
    s.listen(5)

    b64_key = base64.b64encode(secret_key).decode('utf-8')
    port = s.getsockname()[1]

    qrcode.make(f"{ip}&{port}&{b64_key}").save("qr_code.jpg")

    Image.open("qr_code.jpg").show()


def connect_to_client(conn, addr):
    with conn:
        print(f"Connect to {addr}")

        while True:
            try:
                data = conn.recv(1024)
            except Exception:
                print("connection closed")
                break

            if len(data) <= 0:
                continue

            if data.decode('utf-8') == "ping-test":
                print(f"Got ping test from {addr}")
                conn.send("ack".encode("utf-8"))
                continue

            result_string = aes_cipher.AESCipher(secret_key).decrypt(data)
            print(f"Got data {result_string}")

            pyautogui.write(result_string.decode('utf-8'), 0.01)

            conn.send("ack".encode("utf-8"))


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        build_connection_params(s)

        while True:
            conn, addr = s.accept()

            thread.start_new_thread(connect_to_client, (conn, addr))
