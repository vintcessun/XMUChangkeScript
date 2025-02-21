from qreader import QReader
import cv2
import re
import time
import qrcode
import os
import qrcode_terminal


def is_image_by_extension(file_path):
    _, file_extension = os.path.splitext(file_path)
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    return file_extension.lower() in image_extensions


img = None
for e in os.listdir():
    if is_image_by_extension(e):
        img = e
        break

print(f"发现img:{img}")

qreader = QReader()
image = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB)
url = qreader.detect_and_decode(image=image)[0]
time_key = re.search("~[0-9]{10}", url).group()
that_time = int(time_key[1::])
this_time = int(time.time())
product_time = int((this_time - that_time) / 15) * 15 + that_time
this_url = url.replace(time_key, f"~{product_time}")
os.system("cls")
qrcode_terminal.draw(this_url)
while 1:
    if time.time() - product_time >= 15:
        this_time = int(time.time())
        product_time = int((this_time - that_time) / 15) * 15 + that_time
        this_url = url.replace(time_key, f"~{product_time}")
        os.system("cls")
        qrcode_terminal.draw(this_url)
    time.sleep(0.1)
