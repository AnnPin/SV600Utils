#!/usr/bin/env python
# -*- coding:utf-8 -*-

def get_brightness(r, g, b):
    r /= 255.0
    g /= 255.0
    b /= 255.0
    return math.sqrt(r**2 + g**2 + b**2)/math.sqrt(3)
    
if __name__ == '__main__':
    # Pillowのインストール sudo easy_install Pillow
    from PIL import Image, ImageDraw
    from datetime import datetime
    import os
    import math

    # カレントディレクト中からjpgファイルだけを抽出
    files = filter(lambda file: True if file.endswith('.jpg') else False, os.listdir('./'))
 
    print("Detected JPG images...")
    for file in files:
        print file
    print('')

    threshould = 0.99
    print "Current thresould is ", threshould
     
    for file in files:
        print('CURRENT FILE: '+file)
        print('...')
        img_name = file
        img_prefix = img_name[:img_name.rfind('.')]
        img_suffix = img_name[img_name.rfind('.'):]
    
        src = Image.open(img_name) # 画像の読み込み
        src_width, src_height = src.size

        cur = src.crop((0, 0, src_width, src_height))
        cur_width, cur_height = cur.size
        
        for region in ('l', 't', 'r', 'b'):
            finished = False
            while (not finished):
                edge_bright_sum = 0
                edge_bright_num = 0
                control_bright_sum = 0
                control_bright_num = 0

                if (region == 'l'):
                    for x in xrange(0, 5, 1):
                        for y in xrange(0, cur_height, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            edge_bright_sum += bright
                            edge_bright_num += 1
                    for x in xrange(25, 20, -1):
                        for y in xrange(0, cur_height, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            control_bright_sum += bright
                            control_bright_num += 1
                    edge_bright_ave = float( edge_bright_sum / edge_bright_num )
                    control_bright_ave = float( control_bright_sum / control_bright_num )
    
                    print "LEFT:   ", ('%03.5f' % edge_bright_ave), " / ", ('%03.5f' % control_bright_ave), " = ", ('%03.5f' % (edge_bright_ave/control_bright_ave))
                    if (edge_bright_ave/control_bright_ave <= threshould):
                        cur = cur.crop((5, 0, cur_width, cur_height))
                    else:
                        finished = True

                elif (region == 't'):
                    for y in xrange(0, 5, 1):
                        for x in xrange(0, cur_width, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            edge_bright_sum += bright
                            edge_bright_num += 1
                    for y in xrange(25, 20, -1):
                        for x in xrange(0, cur_width, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            control_bright_sum += bright
                            control_bright_num += 1
                    edge_bright_ave = float( edge_bright_sum / edge_bright_num )
                    control_bright_ave = float( control_bright_sum / control_bright_num )
    
                    print "TOP:    ", ('%03.5f' % edge_bright_ave), " / ", ('%03.5f' % control_bright_ave), " = ", ('%03.5f' % (edge_bright_ave/control_bright_ave))
                    if (edge_bright_ave/control_bright_ave <= threshould):
                        cur = cur.crop((0, 5, cur_width, cur_height))
                    else:
                        finished = True
            
                elif (region == 'r'):
                    for x in xrange(cur_width-5, cur_width, 1):
                        for y in xrange(0, cur_height, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            edge_bright_sum += bright
                            edge_bright_num += 1
                    for x in xrange(cur_width-25, cur_width-20, 1):
                        for y in xrange(0, cur_height, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            control_bright_sum += bright
                            control_bright_num += 1
                    edge_bright_ave = float( edge_bright_sum / edge_bright_num )
                    control_bright_ave = float( control_bright_sum / control_bright_num )
    
                    print "RIGHT:  ", ('%03.5f' % edge_bright_ave), " / ", ('%03.5f' % control_bright_ave), " = ", ('%03.5f' % (edge_bright_ave/control_bright_ave))
                    if (edge_bright_ave/control_bright_ave <= threshould):
                        cur = cur.crop((0, 0, cur_width-5, cur_height))
                    else:
                        finished = True
            
                elif (region == 'b'):
                    for y in xrange(cur_height-5, cur_height, 1):
                        for x in xrange(0, cur_width, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            edge_bright_sum += bright
                            edge_bright_num += 1
                    for y in xrange(cur_height-25, cur_height-20, 1):
                        for x in xrange(0, cur_width, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            control_bright_sum += bright
                            control_bright_num += 1
                    edge_bright_ave = float( edge_bright_sum / edge_bright_num )
                    control_bright_ave = float( control_bright_sum / control_bright_num )
    
                    print "BOTTOM: ", ('%03.5f' % edge_bright_ave), " / ", ('%03.5f' % control_bright_ave), " = ", ('%03.5f' % (edge_bright_ave/control_bright_ave))
                    if (edge_bright_ave/control_bright_ave <= threshould):
                        cur = cur.crop((0, 0, cur_width, cur_height-5))
                    else:
                        finished = True
            
                cur_width, cur_height = cur.size
            
        # 削りすぎていないかを確認しておく
        if src_width-cur_width > 50:
            print('CAUTION: Too trimed!')
            exit()
        if src_height-cur_height > 50:
            print('CAUTION: Too trimed!')
            exit()
        print 'Width trim:  ', src_width-cur_width
        print'Height trim: ', src_height-cur_height

        # バックアップ用フォルダが存在しないなら作成
        if (not os.path.exists('bk')):
            os.mkdir('bk')
        
        # 既に重複するファイル名が存在するなら名前に現在時刻を付加してから保存
        if (not os.path.isfile('bk/'+img_name)):
            src.save('bk/'+img_name, quality=100)
        else:
            date = str( datetime.now().strftime("%Y-%m-%d %H-%M-%S") )
            src.save('bk/'+img_prefix+'_'+date+img_suffix, quality=100)
    
        # 編集後のファイルを保存
        cur.save(img_name, quality=100)
        print('')

    print 'Done!'

