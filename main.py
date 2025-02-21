from qreader import QReader
import cv2
import re
import time
import qrcode
import os
import qrcode_terminal
import glob


def get_latest_image(directory):
    # 图片文件扩展名
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"]
    # 搜索目录下的所有图片文件
    image_files = []

    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(directory, ext)))

    if not image_files:
        return None
    latest_image = max(image_files, key=os.path.getmtime)
    return latest_image


img = get_latest_image(".")
if img is None:
    raise FileNotFoundError("没有查找到图片文件，请任意拍摄一张二维码并放置在目录下")
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
