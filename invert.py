#!/usr/bin/env python
# -*- coding:utf-8 -*-

if __name__ == '__main__':
    # Pillowのインストール sudo easy_install Pillow
    from PIL import Image, ImageDraw
    import PIL.ImageOps
    from datetime import datetime
    import os

    # カレントディレクト中からjpgファイルだけを抽出
    files = filter(lambda file: True if file.endswith('.jpg') else False, os.listdir('./'))
 
    print("Detected JPG images...")
    for file in files:
        print file
    print('')
     
    for file in files:
        img_name = file
        src = Image.open(img_name) # 画像の読み込み
        inverted = PIL.ImageOps.invert(src)
        inverted.save(img_name, quality=100)
    print 'Done!'

