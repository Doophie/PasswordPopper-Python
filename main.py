# main.py
import os
import socket
import pyautogui
import qrcode
import base64

HOST = "192.168.0.15"
PORT = 0


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def open_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        ip = get_local_ip()

        s.bind((HOST, PORT))
        s.listen()

        secret_key = base64.b64encode(bytearray(os.urandom(32))).decode('utf-8')
        port = s.getsockname()[1]

        qrcode.make(f"{ip}&{port}&{secret_key}").save("qr_code.jpg")

        conn, addr = s.accept()

        with conn:
            print(f"Connect to {addr}")

            while True:
                data = conn.recv(1024)
                if len(data) <= 0:
                    continue

                result_string = data.decode('utf-8')
                print(f"Got data {result_string}")

                pyautogui.write(result_string, 0.01)

                conn.send(data)


if __name__ == '__main__':
    open_socket()

