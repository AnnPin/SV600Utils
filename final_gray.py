#!/usr/bin/env python
# -*- coding:utf-8 -*-

if __name__ == '__main__':
    # Pillowのインストール sudo easy_install Pillow
    from PIL import Image, ImageDraw, ImageOps
    from datetime import datetime
    import os
    import shutil
    import math

    # カレントディレクト中からjpgファイルだけを抽出
    files = filter(lambda file: True if file.endswith('.jpg') else False, os.listdir('./'))
 
    print("Detected JPG images...")
    for file in files:
        print file
    print('')

    for file in files:
        print('CURRENT FILE: '+file)
        print('...')
        img_name = file
        img_prefix = img_name[:img_name.rfind('.')]
        img_suffix = img_name[img_name.rfind('.'):]
    
        src = Image.open(img_name) # 画像の読み込み
        src_width, src_height = src.size
        margin = 3

        cur = ImageOps.grayscale(src)
    
        # バックアップ用フォルダが存在しないなら作成
        if (not os.path.exists('final_gray_bk')):
            os.mkdir('final_gray_bk')
            
        # 既に重複するファイル名が存在するなら名前に現在時刻を付加してから保存
        if (not os.path.isfile('final_gray_bk/'+img_name)):
            src.save('final_gray_bk/'+img_name, quality=75)
        else:
            date = str( datetime.now().strftime("%Y-%m-%d %H-%M-%S") )
            src.save('final_gray_bk/'+img_prefix+'_'+date+img_suffix, quality=75)
        
        # 編集後のファイルを保存
        cur.save(img_name, quality=75)
        print('')

    print 'Done!'

