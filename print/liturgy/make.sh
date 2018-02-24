source ../../../../dev/devevn/bin/activate

python ../prayer-to-tex.py index-st-paul.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/ st-paul-hymn-en.tex
python ../prayer-to-tex.py index-st-paul.xml ../../android_prayer_book/app/src/main/assets/prayers/la/src/ st-paul-hymn-la.tex

lualatex --shell-escape st-paul-novena-en.tex
lualatex --shell-escape st-paul-novena-la.tex

#python ../prayer-to-tex.py ../../android_prayer_book/app/src/main/assets/prayers/en/src/renewal-covenant.html renewal-covenant.tex
#lualatex --shell-escape renewal-covenant.tex

#python ../prayer-to-tex.py ../../android_prayer_book/app/src/main/assets/prayers/en/src/lectionary/australia-day.html australia-day.tex
#lualatex --shell-escape australia-day.tex


python ../prayer-to-tex.py liturgy-index.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/mass/ mass/
python ../prayer-to-tex.py liturgy-index.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/mass/ liturgy.tex

python ../prayer-to-tex.py lectionary-index.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/lectionary/ lectionary
python ../prayer-to-tex.py lectionary-index.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/lectionary/ lectionary.tex

python ../prayer-to-tex.py office-index.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/office/ office.tex

python ../prayer-to-tex.py ceremonial-index.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/ceremonial/ ceremonial.tex


lualatex --shell-escape liturgy-book.tex
lualatex --shell-escape lectionary-book.tex
lualatex --shell-escape ceremonial-book.tex
lualatex --shell-escape office-book.tex
lualatex --shell-escape mary-queen-of-hermits.tex
lualatex --shell-escape saint-paul-the-first-hermit.tex
lualatex --shell-escape blessed-eusebius.tex
lualatex --shell-escape renewal-vows.tex
lualatex --shell-escape renewal-covenant.tex
