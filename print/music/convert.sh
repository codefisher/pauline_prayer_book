lualatex --shell-escape "$1"
lualatex --shell-escape "$1"
convert -density 300 -trim "${1/%.tex/}.pdf" -quality 100 -flatten "${1/%.tex/}.png"
pdf2svg "${1/%.tex/}.pdf" "${1/%.tex/}.svg"

sed -i -r 's/^(<svg .* )width=".*pt" height=".*pt"/\1/' "${1/%.tex/}.svg"

for f in *.svg ; do
cp "$f" "../../android_prayer_book/app/src/main/assets/prayers/music/$f"; done

