from ppadb.client import Client as AdbClient

import time

import cv2

import pytesseract

import cv2 as opencv

import numpy as np

import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from PIL import Image

print("Nhập thứ tự giả lập")
thutu = input()
thutu = int(thutu)
print("Nhập vị trí bắt đầu")
vitri = input()
vitri = int(vitri)
def suaanh(img):
    im = Image.open(img + ".png")
    im = im.convert("P")
    im2 = Image.new("P",im.size,0)

    im = im.convert("P")

    temp = {}

    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y,x))
            temp[pix] = pix
            if pix > 130: # Đây là các màu được lấy_
                im2.putpixel((y,x),255)

    im2.save(img + ".gif")
os.system('adb devices')
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
device = client.device(devices[thutu - 1].serial)
listtoado = {
    "x":['120','270','420'],
    "y":['160','300','453'],
}
lan = 1
saiso = 0
while True:
    for i in range(1,4):
        a = 78 + 85*(i - 1)
        b = 130 + saiso + 73*(lan - 1)
        device.input_tap(a, b)
        time.sleep(3)
        result = device.screencap()
        with open("data/screen-" + str(vitri) + "-" + str(i) + ".png", "wb") as fp:
            fp.write(result)
        IMG_PATH = "data/screen-" + str(vitri) + "-" + str(i) + ".png"
        img = cv2.imread(IMG_PATH)
        img_crop = img[560:587, 180:480, :]
        crop_name = "data/screencrop-" + str(vitri) + "-" + str(i) + ".png"
        cv2.imwrite(crop_name, img_crop)
        suaanh("data/screencrop-" + str(vitri) + "-" + str(i))
        lm_crop = img[630:655, 46:345, :]
        crop_lm = "data/lienminh-" + str(vitri) + "-" + str(i) + ".png"
        cv2.imwrite(crop_lm, lm_crop)
        suaanh("data/lienminh-" + str(vitri) + "-" + str(i))
        pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR/tesseract'
        text1 = pytesseract.image_to_string(r"data/screencrop-" + str(vitri) + "-" + str(i) + ".gif",config='--psm 6',lang='vie')
        if text1.find('(') == -1:
            text1 = pytesseract.image_to_string(r"data/screencrop-" + str(vitri) + "-" + str(i) + ".png",config='--psm 7',lang='vie')
        text2 = pytesseract.image_to_string(r"data/lienminh-" + str(vitri) + "-" + str(i) + ".png",config='--psm 6',lang='vie')
        text3 = pytesseract.image_to_string(r"data/lienminh-" + str(vitri) + "-" + str(i) + ".gif",config='--psm 7',lang='vie')
        with open('data' + str(thutu)  + '.txt', 'a+', encoding='utf-8') as f:
                f.write(str(vitri) + "-" + str(i) + ':' + text1[text1.find('('):text1.find(')') + 1] + ':' + text2[text2.find(':') + 1:len(text2) - 2] + ' (' + text3[text3.find(':') + 1:len(text3) - 2] + ')' + '\n')
        device.input_tap(573,130)
    for i in range(4,7):
            a = 380 + 85*(i - 4)
            b = 135 + saiso + 72*(lan - 1)
            device.input_tap(a, b)
            time.sleep(3)
            result = device.screencap()
            with open("data/screen-" + str(vitri) + "-" + str(i) + ".png", "wb") as fp:
                fp.write(result)
            IMG_PATH = "data/screen-" + str(vitri) + "-" + str(i) + ".png"
            img = cv2.imread(IMG_PATH)
            img_crop = img[560:585, 180:480, :]
            crop_name = "data/screencrop-" + str(vitri) + "-" + str(i) + ".png"
            cv2.imwrite(crop_name, img_crop)
            suaanh("data/screencrop-" + str(vitri) + "-" + str(i))
            lm_crop = img[630:657, 46:345, :]
            crop_lm = "data/lienminh-" + str(vitri) + "-" + str(i) + ".png"
            cv2.imwrite(crop_lm, lm_crop)
            suaanh("data/lienminh-" + str(vitri) + "-" + str(i))
            pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR/tesseract'
            text1 = pytesseract.image_to_string(r"data/screencrop-" + str(vitri) + "-" + str(i) + ".gif",config='--psm 6',lang='vie')
            if text1.find('(') == -1:
                text1 = pytesseract.image_to_string(r"data/screencrop-" + str(vitri) + "-" + str(i) + ".png",config='--psm 7',lang='vie')
            text2 = pytesseract.image_to_string(r"data/lienminh-" + str(vitri) + "-" + str(i) + ".png",config='--psm 6',lang='vie')
            text3 = pytesseract.image_to_string(r"data/lienminh-" + str(vitri) + "-" + str(i) + ".gif",config='--psm 7',lang='vie')
            with open('data' + str(thutu)  + '.txt', 'a+', encoding='utf-8') as f:
                f.write(str(vitri) + "-" + str(i) + ':' + text1[text1.find('('):text1.find(')') + 1] + ':' + text2[text2.find(':') + 1:len(text2) - 2] + ' (' + text3[text3.find(':') + 1:len(text3) - 2] + ')' + '\n')
            device.input_tap(573,130)
    lan += 1
    if lan == 11:
        device.shell("input swipe 80 845 75 125 5000")
        lan = 1
    vitri += 1
    if vitri == 112:
        lan +=1
        # saiso = 10