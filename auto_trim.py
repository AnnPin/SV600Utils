#!/usr/bin/env python
# -*- coding:utf-8 -*-

def get_brightness (r, g, b):
    r /= 255.0
    g /= 255.0
    b /= 255.0
    return math.sqrt(r**2 + g**2 + b**2)/math.sqrt(3)
    
def get_weight (x, y, width, height):
    x_weight = 1.0 + 1.0 * ( abs(x-width/2.0) ) / (width/2.0)
    y_weight = 1.0 + 1.0 * ( abs(y-height/2.0) ) / (height/2.0)
    return x_weight * y_weight

if __name__ == '__main__':
    # Pillowのインストール sudo easy_install Pillow
    from PIL import Image, ImageDraw
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

    threshould = 0.99
    target = 5
    control = 50
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
        
        # 平均的にスコアを算出する
        print('Average method:')
        for region in ('l', 't', 'r', 'b'):
            finished = False
            while (not finished):
                edge_bright_sum = 0
                edge_bright_num = 0
                control_bright_sum = 0
                control_bright_num = 0

                if (region == 'l'):
                    for x in xrange(0, target, 1):
                        for y in xrange(0, cur_height, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            edge_bright_sum += bright
                            edge_bright_num += 1
                    for x in xrange(control, control-target, -1):
                        for y in xrange(0, cur_height, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            control_bright_sum += bright
                            control_bright_num += 1
                    edge_bright_ave = float( edge_bright_sum / edge_bright_num )
                    control_bright_ave = float( control_bright_sum / control_bright_num )
    
                    print "LEFT:   ", ('%03.5f' % edge_bright_ave), " / ", ('%03.5f' % control_bright_ave), " = ", ('%03.5f' % (edge_bright_ave/control_bright_ave))
                    if (edge_bright_ave/control_bright_ave <= threshould):
                        cur = cur.crop((target, 0, cur_width, cur_height))
                    else:
                        finished = True

                elif (region == 't'):
                    for y in xrange(0, target, 1):
                        for x in xrange(0, cur_width, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            edge_bright_sum += bright
                            edge_bright_num += 1
                    for y in xrange(control, control-target, -1):
                        for x in xrange(0, cur_width, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            control_bright_sum += bright
                            control_bright_num += 1
                    edge_bright_ave = float( edge_bright_sum / edge_bright_num )
                    control_bright_ave = float( control_bright_sum / control_bright_num )
    
                    print "TOP:    ", ('%03.5f' % edge_bright_ave), " / ", ('%03.5f' % control_bright_ave), " = ", ('%03.5f' % (edge_bright_ave/control_bright_ave))
                    if (edge_bright_ave/control_bright_ave <= threshould):
                        cur = cur.crop((0, target, cur_width, cur_height))
                    else:
                        finished = True
            
                elif (region == 'r'):
                    for x in xrange(cur_width-target, cur_width, 1):
                        for y in xrange(0, cur_height, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            edge_bright_sum += bright
                            edge_bright_num += 1
                    for x in xrange(cur_width-control, cur_width-(control-target), 1):
                        for y in xrange(0, cur_height, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            control_bright_sum += bright
                            control_bright_num += 1
                    edge_bright_ave = float( edge_bright_sum / edge_bright_num )
                    control_bright_ave = float( control_bright_sum / control_bright_num )
    
                    print "RIGHT:  ", ('%03.5f' % edge_bright_ave), " / ", ('%03.5f' % control_bright_ave), " = ", ('%03.5f' % (edge_bright_ave/control_bright_ave))
                    if (edge_bright_ave/control_bright_ave <= threshould):
                        cur = cur.crop((0, 0, cur_width-target, cur_height))
                    else:
                        finished = True
            
                elif (region == 'b'):
                    for y in xrange(cur_height-target, cur_height, 1):
                        for x in xrange(0, cur_width, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            edge_bright_sum += bright
                            edge_bright_num += 1
                    for y in xrange(cur_height-control, cur_height-(control-target), 1):
                        for x in xrange(0, cur_width, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            control_bright_sum += bright
                            control_bright_num += 1
                    edge_bright_ave = float( edge_bright_sum / edge_bright_num )
                    control_bright_ave = float( control_bright_sum / control_bright_num )
    
                    print "BOTTOM: ", ('%03.5f' % edge_bright_ave), " / ", ('%03.5f' % control_bright_ave), " = ", ('%03.5f' % (edge_bright_ave/control_bright_ave))
                    if (edge_bright_ave/control_bright_ave <= threshould):
                        cur = cur.crop((0, 0, cur_width, cur_height-target))
                    else:
                        finished = True
            
                cur_width, cur_height = cur.size
            
        # 隅の方に重みを持たせて再度スコアを計算する
        print('Weighting method:')
        for region in ('l', 't', 'r', 'b'):
            finished = False
            while (not finished):
                edge_bright_sum = 0
                edge_bright_num = 0
                control_bright_sum = 0
                control_bright_num = 0

                if (region == 'l'):
                    for x in xrange(0, target, 1):
                        for y in xrange(0, cur_height, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            bright *= get_weight(x, y, cur_width, cur_height)
                            edge_bright_sum += bright
                            edge_bright_num += 1
                    for x in xrange(control, control-target, -1):
                        for y in xrange(0, cur_height, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            bright *= get_weight(x, y, cur_width, cur_height)
                            control_bright_sum += bright
                            control_bright_num += 1
                    edge_bright_ave = float( edge_bright_sum / edge_bright_num )
                    control_bright_ave = float( control_bright_sum / control_bright_num )
    
                    print "LEFT:   ", ('%03.5f' % edge_bright_ave), " / ", ('%03.5f' % control_bright_ave), " = ", ('%03.5f' % (edge_bright_ave/control_bright_ave))
                    if (edge_bright_ave/control_bright_ave <= threshould):
                        cur = cur.crop((target, 0, cur_width, cur_height))
                    else:
                        finished = True

                elif (region == 't'):
                    for y in xrange(0, target, 1):
                        for x in xrange(0, cur_width, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            bright *= get_weight(x, y, cur_width, cur_height)
                            edge_bright_sum += bright
                            edge_bright_num += 1
                    for y in xrange(control, control-target, -1):
                        for x in xrange(0, cur_width, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            bright *= get_weight(x, y, cur_width, cur_height)
                            control_bright_sum += bright
                            control_bright_num += 1
                    edge_bright_ave = float( edge_bright_sum / edge_bright_num )
                    control_bright_ave = float( control_bright_sum / control_bright_num )
    
                    print "TOP:    ", ('%03.5f' % edge_bright_ave), " / ", ('%03.5f' % control_bright_ave), " = ", ('%03.5f' % (edge_bright_ave/control_bright_ave))
                    if (edge_bright_ave/control_bright_ave <= threshould):
                        cur = cur.crop((0, target, cur_width, cur_height))
                    else:
                        finished = True
            
                elif (region == 'r'):
                    for x in xrange(cur_width-target, cur_width, 1):
                        for y in xrange(0, cur_height, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            bright *= get_weight(x, y, cur_width, cur_height)
                            edge_bright_sum += bright
                            edge_bright_num += 1
                    for x in xrange(cur_width-control, cur_width-(control-target), 1):
                        for y in xrange(0, cur_height, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            bright *= get_weight(x, y, cur_width, cur_height)
                            control_bright_sum += bright
                            control_bright_num += 1
                    edge_bright_ave = float( edge_bright_sum / edge_bright_num )
                    control_bright_ave = float( control_bright_sum / control_bright_num )
    
                    print "RIGHT:  ", ('%03.5f' % edge_bright_ave), " / ", ('%03.5f' % control_bright_ave), " = ", ('%03.5f' % (edge_bright_ave/control_bright_ave))
                    if (edge_bright_ave/control_bright_ave <= threshould):
                        cur = cur.crop((0, 0, cur_width-target, cur_height))
                    else:
                        finished = True
            
                elif (region == 'b'):
                    for y in xrange(cur_height-target, cur_height, 1):
                        for x in xrange(0, cur_width, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            bright *= get_weight(x, y, cur_width, cur_height)
                            edge_bright_sum += bright
                            edge_bright_num += 1
                    for y in xrange(cur_height-control, cur_height-(control-target), 1):
                        for x in xrange(0, cur_width, 1):
                            bright = get_brightness( *cur.getpixel((x, y)) )
                            bright *= get_weight(x, y, cur_width, cur_height)
                            control_bright_sum += bright
                            control_bright_num += 1
                    edge_bright_ave = float( edge_bright_sum / edge_bright_num )
                    control_bright_ave = float( control_bright_sum / control_bright_num )
    
                    print "BOTTOM: ", ('%03.5f' % edge_bright_ave), " / ", ('%03.5f' % control_bright_ave), " = ", ('%03.5f' % (edge_bright_ave/control_bright_ave))
                    if (edge_bright_ave/control_bright_ave <= threshould):
                        cur = cur.crop((0, 0, cur_width, cur_height-target))
                    else:
                        finished = True
            
                cur_width, cur_height = cur.size
            
            
        # 削りすぎていないかを確認しておく
        if src_width-cur_width > 25 or src_height-cur_height > 25:
            print('CAUTION: Too trimed!')
            if (not os.path.exists('too_trim')):
                os.mkdir('too_trim')
            if (not os.path.isfile('too_trim/trim.command')):
                shutil.copy('trim.command', 'too_trim')
                shutil.copy('trim.py', 'too_trim')
            shutil.move(img_name, 'too_trim/'+img_name)
            
        else:
            print 'Width trim:  ', src_width-cur_width
            print'Height trim: ', src_height-cur_height
    
            # バックアップ用フォルダが存在しないなら作成
            if (not os.path.exists('auto_trim_bk')):
                os.mkdir('auto_trim_bk')
            
            # 既に重複するファイル名が存在するなら名前に現在時刻を付加してから保存
            if (not os.path.isfile('auto_trim_bk/'+img_name)):
                src.save('auto_trim_bk/'+img_name, quality=75)
            else:
                date = str( datetime.now().strftime("%Y-%m-%d %H-%M-%S") )
                src.save('auto_trim_bk/'+img_prefix+'_'+date+img_suffix, quality=75)
        
            # 編集後のファイルを保存
            cur.save(img_name, quality=75)
        print('')

    print 'Done!'

