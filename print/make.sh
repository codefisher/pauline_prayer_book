
python3 ../android_prayer_book/app/src/main/assets/prayers/convert_html.py -p --output=prayers --input=../android_prayer_book/app/src/main/assets/prayers/en/src/
python3 ../android_prayer_book/app/src/main/assets/prayers/convert_html.py -p --output=prayers --input=../android_prayer_book/app/src/main/assets/prayers/en/print/


cd prayers
for f in *.html ; do wkhtmltopdf --page-width 5in --page-height 8in "$f" "../pdf/${f/%.html/}.pdf" ; done

cd ../

rm book.aux
rm book.log
rm book.out

pdflatex book.tex
pdflatex book.tex
