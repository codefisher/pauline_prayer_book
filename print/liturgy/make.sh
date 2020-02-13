source ../../../../dev/devevn/bin/activate

python ../prayer-to-tex.py index-st-paul.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/ st-paul-hymn-en.tex
python ../prayer-to-tex.py index-st-paul.xml ../../android_prayer_book/app/src/main/assets/prayers/la/src/ st-paul-hymn-la.tex

lualatex --shell-escape st-paul-novena-en.tex
lualatex --shell-escape st-paul-novena-la.tex

#python ../prayer-to-tex.py ../../android_prayer_book/app/src/main/assets/prayers/en/src/renewal-covenant.html renewal-covenant.tex
#lualatex --shell-escape renewal-covenant.tex

#python ../prayer-to-tex.py ../../android_prayer_book/app/src/main/assets/prayers/en/src/lectionary/australia-day.html australia-day.tex
#lualatex --shell-escape australia-day.tex


python ../prayer-to-tex.py liturgy-index.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/mass/ mass/ --nomusic
python ../prayer-to-tex.py liturgy-index.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/mass/ liturgy.tex --nomusic --noimages
python ../prayer-to-tex.py liturgy-index-la.xml ../../android_prayer_book/app/src/main/assets/prayers/la/src/mass/ liturgy-la.tex

python ../prayer-to-tex.py missal.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/mass/ missal.tex
python ../prayer-to-tex.py shrines.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/mass/ shrines.tex

python ../prayer-to-tex.py constitutions.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/constitutions/ constitutions.tex
python ../prayer-to-tex.py constitutions-la.xml ../../android_prayer_book/app/src/main/assets/prayers/la/src/constitutions/ constitutions-la.tex


python ../prayer-to-tex.py extraordinary-form.xml ../../android_prayer_book/app/src/main/assets/prayers/la/src/extraordinary-form/ extraordinary-form.tex
python ../prayer-to-tex.py extraordinary-missal.xml ../../android_prayer_book/app/src/main/assets/prayers/la/src/extraordinary-form/ extraordinary-missal.tex
python ../prayer-to-tex.py extraordinary-form-la-en.xml ../../android_prayer_book/app/src/main/assets/prayers/la/src/extraordinary-form/ extraordinary-form-la-en.tex


python ../prayer-to-tex.py lectionary-index.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/lectionary/ lectionary
python ../prayer-to-tex.py lectionary-index.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/lectionary/ lectionary.tex --noimages
python ../prayer-to-tex.py lectionary-index-la.xml ../../android_prayer_book/app/src/main/assets/prayers/la/src/lectionary/ lectionary-la.tex

python ../prayer-to-tex.py office-index.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/office/ office.tex
python ../prayer-to-tex.py office-index.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/office/ office/
python ../prayer-to-tex.py office-blessed-eusebius.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/office/ office-blessed-eusebius.tex
python ../prayer-to-tex.py office-review.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/office/ office-review.tex --noimages

python ../prayer-to-tex.py ceremonial-index.xml ../../android_prayer_book/app/src/main/assets/prayers/en/src/ceremonial/ ceremonial.tex

lualatex --shell-escape liturgy-book.tex
lualatex --shell-escape extraordinary-form-book.tex
lualatex --shell-escape extraordinary-missal-book.tex
lualatex --shell-escape extraordinary-form-la-en-book.tex
lualatex --shell-escape missal-book.tex
lualatex --shell-escape constitutions-book.tex
lualatex --shell-escape constitutions-book-la.tex
lualatex --shell-escape shrines-book.tex
lualatex --shell-escape conventual-general-intercessions.tex
lualatex --shell-escape vocation-intercessions.tex
lualatex --shell-escape liturgy-book-la.tex
lualatex --shell-escape lectionary-book.tex
lualatex --shell-escape lectionary-book-la.tex
lualatex --shell-escape ceremonial-book.tex
lualatex --shell-escape office-blessed-eusebius-book.tex
lualatex --shell-escape liturgy-book.tex
lualatex --shell-escape mary-queen-of-hermits.tex
lualatex --shell-escape saint-paul-the-first-hermit.tex
lualatex --shell-escape blessed-eusebius.tex
lualatex --shell-escape renewal-vows.tex
lualatex --shell-escape renewal-covenant.tex
lualatex --shell-escape office-book.tex
lualatex --shell-escape office-review-book.tex