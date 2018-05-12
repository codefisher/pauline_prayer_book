source ../../../dev/devevn/bin/activate

python prayer-to-tex.py index.xml ../android_prayer_book/app/src/main/assets/prayers/en/src/ prayer-book-content.tex

#lualatex --shell-escape prayer-document.tex
lualatex --shell-escape prayer-book.tex


gs -o prayer-book-low.pdf -sDEVICE=pdfwrite -r100 prayer-book.pdf

#gs -o prayer-book-cmyk.pdf -sDEVICE=pdfwrite -sProcessColorModel=DeviceCMYK  -dOverrideICC=true  -sColorConversionStrategy=CMYK -sColorConversionStrategyForImages=CMYK -dPDFSETTINGS=/prepress -dAutoFilterColorImages=false -dColorImageFilter=/FlateEncode -r300 prayer-book.pdf

#gs -o prayer-book-low-cmyk.pdf -dPDFX -sDEVICE=pdfwrite -sProcessColorModel=DeviceCMYK  -dOverrideICC=true  -sColorConversionStrategy=CMYK -sColorConversionStrategyForImages=CMYK -dPDFSETTINGS=/prepress -dAutoFilterColorImages=false -dColorImageFilter=/FlateEncode -r100 prayer-book.pdf

#gs -o 2370000545633-Case-cmyk.pdf -dPDFX -sDEVICE=pdfwrite -sProcessColorModel=DeviceCMYK  -dOverrideICC=true  -sColorConversionStrategy=CMYK -sColorConversionStrategyForImages=CMYK -dPDFSETTINGS=/prepress -dAutoFilterColorImages=false -dColorImageFilter=/FlateEncode 2370000545633-Case.pdf
