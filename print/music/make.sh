for f in *.tex ; do
lualatex --shell-escape "$f"
lualatex --shell-escape "$f"
convert -density 300 -trim "${f/%.tex/}.pdf" -quality 100 -flatten "${f/%.tex/}.png"
pdf2svg "${f/%.tex/}.pdf" "${f/%.tex/}.svg"; done

for f in *.ly ; do 
lilypond -fpdf "$f"
convert -density 300 -trim "${f/%.ly/}.pdf" -quality 100 -flatten "${f/%.ly/}.png"
pdf2svg "${f/%.ly/}.pdf" "${f/%.ly/}.svg"; done

#needed since on Android having width and height cause sizing problesm
#this removes them and leaves just the viewBox attribute for sizing
sed -i -r 's/^(<svg .* )width=".*pt" height=".*pt"/\1/' *.svg

for f in *.svg ; do
cp "$f" "../../android_prayer_book/app/src/main/assets/prayers/music/$f"; done

#convert -density 300 -crop 1200x228 agnus-die.pdf agnus-die-line-%d.pdf