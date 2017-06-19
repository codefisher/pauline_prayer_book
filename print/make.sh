python3 prayer-to-tex.py index.xml ../android_prayer_book/app/src/main/assets/prayers/en/src/ prayer-book-content.tex

lualatex --shell-escape prayer-book.tex


gs -o prayer-book-cmyk.pdf -dPDFX -sDEVICE=pdfwrite -sProcessColorModel=DeviceCMYK  -dOverrideICC=true  -sColorConversionStrategy=CMYK -sColorConversionStrategyForImages=CMYK -dPDFSETTINGS=/prepress -dAutoFilterColorImages=false -dColorImageFilter=/FlateEncode prayer-book.pdf
