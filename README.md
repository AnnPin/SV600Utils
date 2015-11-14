ScanSnap SV600 の画像補正を支援するためのスクリプトたち
=======================================================

*  For MacOSX Only!
*  PFU ScanSnap SV600で取り込んだ書類データの補正を出来るだけ早く行うために作成したスクリプト集 (完全な個人用なので殴り書き)
*  PDFファイルを一旦画像データとして分割してしまい、一つ一つの画像データに対してトリミングを高速に行える

Contents
--------
*  pdf2jpg.command
    -  ダブルクリックで実行することで、input.pdfという名前のPDFファイルから中に含まれているJPGファイルをimgから始まるファイル名で取り出す
    -  pdfimagesコマンドを使うので、Homebrewを使ってxpdfをインストールしてください
        +  `brew install xpdf`

*  jpg2pdf.command
    -  ダブルクリックで実行することで、ディレクトリ中に存在している"img"から始まる全てのJPGファイルをoutput.pdfにまとめる
    -  convertコマンドを使うので、Homebrewを使ってImagemagickをインストールしてください
        +  `brew install imagemagick`

*  invert.command / invert.py
    -  invert.commandをダブルクリックで実行することでinvert.pyを実行し、ディレクトリ中に存在している"img"から始まる全てのJPGファイルをネガポジ反転する
    -  ノイズ除去時に便利
    -  Pythonスクリプト中でPillowモジュールを使用するので、あらかじめインストールをしておいてください
        +  `sudo easy_install Pillow`

*  trim.command / trim.py
    -  trim.commandをダブルクリックで実行することでtrim.pyを実行し、ディレクトリ中に存在している"img"から始まる全てのJPGファイルに対して四隅のトリミングをコマンドラインで実行できる
    -  "左隅を50px、右隅を20pxトリミングしたい"場合、シェル上で"l50 r20"と入力してください
    -  Pythonスクリプト中でPillowモジュールを使用するので、あらかじめインストールをしておいてください
        +  `sudo easy_install Pillow`

