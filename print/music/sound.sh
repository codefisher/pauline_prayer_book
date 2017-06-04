for f in *.gabc ; do ~/Downloads/gabc2mid-master/sound.sh "$f" 
rm sound/*.mid
rm sound/*.wav; done
