source ../../../../dev/devevn/bin/activate

python ../prayer-to-tex.py index.xml html/ hymn-book-content.tex

lualatex --shell-escape hymn-book.tex

gs -o hymn-book-cmyk.pdf -dPDFX -sDEVICE=pdfwrite -sProcessColorModel=DeviceCMYK  -dOverrideICC=true  -sColorConversionStrategy=CMYK -sColorConversionStrategyForImages=CMYK -dPDFSETTINGS=/prepress -dAutoFilterColorImages=false -dColorImageFilter=/FlateEncode hymn-book.pdf

gs -o 2370000426406-Perfect-cmyk.pdf -dPDFX -sDEVICE=pdfwrite -sProcessColorModel=DeviceCMYK  -dOverrideICC=true  -sColorConversionStrategy=CMYK -sColorConversionStrategyForImages=CMYK -dPDFSETTINGS=/prepress -dAutoFilterColorImages=false -dColorImageFilter=/FlateEncode 2370000426406-Perfect-272.pdf
