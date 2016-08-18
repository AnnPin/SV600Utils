#!/bin/sh

cd `dirname $0`
jpgs="img*.jpg"
for jpgpath in $jpgs; do
  number=$jpgpath
  number=${number#img-}
  number=${number%%.*}
  echo "Generating output-${number}.pdf..."
  convert -verbose $jpgpath output-${number}.pdf
done

echo "Generating output.pdf..."
pdftk output-*.pdf cat output output.pdf
#convert -verbose output-*.pdf output.pdf 

echo "Removing tmp files..."
rm ./output-*.pdf

