#!/usr/bin/env python
# -*- coding:utf-8 -*-

if __name__ == '__main__':
    # Pillowのインストール sudo easy_install Pillow
    from PIL import Image, ImageDraw
    from datetime import datetime
    import os

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
        cur = src.crop((0, 0, src_width, src_height))
        
        cmd = None
        undo_stack = []
        redo_stack = []
        while (cmd != 'n'):
            
            cur_width, cur_height = cur.size
            grided = cur.crop((0, 0, cur_width, cur_height))

            # グリッド
            # Blue: 25x25
            # Red : 50x50
            grid = ImageDraw.Draw(grided)
            for i, row in enumerate( xrange(0, cur_height/10, 25) ):
                if (i % 2 == 0):
                    grid.line(((0, row), (cur_width, row)), (255, 128, 128), 1)
                else:
                    grid.line(((0, row), (cur_width, row)), (128, 128, 256), 1)

            for i, row in enumerate( xrange(cur_height-1, 9*cur_height/10, -25) ):
                if (i % 2 == 0):
                    grid.line(((0, row), (cur_width, row)), (255, 128, 128), 1)
                else:
                    grid.line(((0, row), (cur_width, row)), (128, 128, 256), 1)

            for i, col in enumerate( xrange(0, cur_width/10, 25) ):
                if (i % 2 == 0):
                    grid.line(((col, 0), (col, cur_height)), (255, 128, 128), 1)
                else:
                    grid.line(((col, 0), (col, cur_height)), (128, 128, 256), 1)

            for i, col in enumerate( xrange(cur_width-1, 9*cur_width/10, -25) ):
                if (i % 2 == 0):
                    grid.line(((col, 0), (col, cur_height)), (255, 128, 128), 1)
                else:
                    grid.line(((col, 0), (col, cur_height)), (128, 128, 256), 1)

            grided.show() # 画像の表示
        
            print('Input your command.')
            print('  format:')
            print('    [ltrb][0-9][1-9]* : trim the range')
            print('    z : undo')
            print('    Z : redo')
            print('    c : clear your edit')
            # print('    p : previous image')
            print('    n : next image')
            print('    e : quit')
            print('    q : quit')
            cmd = raw_input('>>> ')
        
            cmd_list = cmd.split(" ")
            
            if (len(cmd_list) == 1):
                if (cmd_list[0] == 'z'):
                    # Undo
                    if (len(undo_stack) > 0):
                        redo_stack.append(cur)
                        cur = undo_stack.pop()
                    else:
                        pass
            
                elif (cmd_list[0] == 'Z'):
                    # Redo
                    if (len(redo_stack) > 0):
                        undo_stack.append(cur)
                        cur = redo_stack.pop()
                    else:
                        pass
            
                elif (cmd_list[0] == 'c'):
                    # Clear
                    cur = src.crop((0, 0, src_width, src_height))
                    undo_stack = []
                    redo_stack = []
            
                # elif (cmd_list[0] == 'p'):
                #     pass
            
                elif (cmd_list[0] == 'n'):
                    pass
            
                elif (cmd_list[0] == 'e' or cmd_list[0] == 'q'):
                    print('Interrupted...')
                    print('Bye.');
                    exit()
            else:
                undo_stack.append(cur)
                redo_stack = []
                for token in cmd_list:
                    print token
                    if (len(token) == 1):
                        token = token + '0'
                    value = int(token[1:])
                    if (token[0] == 'l'):
                        cur = cur.crop((value, 0, cur_width, cur_height))
                    elif (token[0] == 't'):
                        cur = cur.crop((0, value, cur_width, cur_height))
                    elif (token[0] == 'r'):
                        cur = cur.crop((0, 0, cur_width-value, cur_height))
                    elif (token[0] == 'b'):
                        cur = cur.crop((0, 0, cur_width, cur_height-value))
                    else:
                        print('Invalid command!')
                    cur_width, cur_height = cur.size
        
        
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

    print 'Done!'

