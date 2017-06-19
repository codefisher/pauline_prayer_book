for f in *.ly ; do 
lilypond -fpdf "$f"
convert -density 300 -trim "${f/%.ly/}.pdf" -quality 100 -flatten "images/${f/%.ly/}.png"
pdf2svg "${f/%.ly/}.pdf" "images/${f/%.ly/}.svg"; done

mv *.midi sound/

cd images

#needed since on Android having width and height cause sizing problesm
#this removes them and leaves just the viewBox attribute for sizing
sed -i -r 's/^(<svg .* )width=".*pt" height=".*pt"/\1/' *.svg

for f in *.svg ; do
cp "$f" "../../../android_prayer_book/app/src/main/assets/prayers/music/$f"; done

for f in *.lytex ; do 
lilypond-book --pdf --output=lilypond --format=latex "$f";
done

#convert -density 300 -crop 1200x228 agnus-die.pdf agnus-die-line-%d.pdf
