\version "2.18.2"

#(set! paper-alist (cons '("boolet size" . (cons (* 7 in) (* 3.5 in))) paper-alist))

\paper {
   #(set-paper-size "boolet size")
   indent = 0
   ragged-last = ##f
   top-margin = 0
   bottom-margin = 0
   right-margin = 0
   left-margin = 5\mm
} 

\header {
  tagline = ""  % removed
}

musicOne = \relative c' {
  \autoBeamOff
  \time 3/4
  c'4 c4 c4 \bar "|" a8[g8] f4 r4 \bar "|" g4 f4 d4 \bar "|" c4 c2 \bar "|" d4 e4 f4 \bar "|" d4 e4 f4 \bar "|" a2. \bar "|" g2 r4 \bar "|" \break
  c4 c4 c4 \bar "|" a8[g8] f4 r4 \bar "|" g4 f4 d4 \bar "|" c4 c2 \bar "|" d4 e4 f4 \bar "|" g4 f4 e4 \bar "|" f2 r4 \bar "|" \break
  \bar ".|:" g4 g4 g4 \bar "|" g4 f4 g4 \bar "|" a2. \bar "|" c2 r4 \bar "|" g4 g4 g4 \bar "|" g4 f4 g4 \bar "|" a2. \bar "|" \break
  c4 c4 c4 \bar "|" a8[g8] f4 r4 \bar "|" g4 e4 d4 \bar "|" c2 r4 \bar "|" d4 e4 f4 \bar "|" g4 f4 e4 \bar "|" f2. \bar ":|."
}

verseOne = \lyricmode {
  Świę -- ty nasz O -- jcze Pa -- wle "z pu" -- sty -- ne, wspie -- raj nas swo -- ją mo -- dli -- twą,
  by Bia -- li Bra -- cia, sy -- no -- wie Two -- i, nie -- śli na świat do -- brą Wieść!
  Zba -- vie -- niem na -- szym jest Chry -- stus, dzie -- dzi -- ctwem na -- szym On Sam.
  Pa -- wle, nasz O -- jcze, chce -- me jak Ty wy -- znać, że Jezus to Pan!
}

\score {
  <<
    \new Voice = "one" {
      \override Score.BarNumber #'Y-offset = #2
    \override Score.BarNumber #'outside-staff-priority = ##f
    \override Score.BarNumber #'break-visibility = #'#(#f #f #t)
    \clef treble 
    \key f \major
     \musicOne
    }
    \new Lyrics \lyricsto "one" {
      <<
      { \verseOne }
      >>

    }
  >>
}