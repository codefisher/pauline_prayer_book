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
  c'4 c4 c4 \bar "|" a8[g8] f4 r4 \bar "|" g4 f4 d4 \bar "|" c4 r2 \bar "|" d4 e4 f4 \bar "|" d4 e4 f4 \bar "|" a2. \bar "|" g2 r4 \bar "|" \break
  c4 c4 c4 \bar "|" a8[g8] f4 r4 \bar "|" g4 f4 d4 \bar "|" c4 r2 \bar "|" d4 e4 f4 \bar "|" g4 f4 e4 \bar "|" f2 r4 \bar "|" \break
  \bar ".|:" g4 g4 g4 \bar "|" g4 f4 g4 \bar "|" a2. \bar "|" c2 r4 \bar "|" g4 g4 g4 \bar "|" g4 f4 g4 \bar "|" a2. \bar "|" \break
  c4 c4 c4 \bar "|" a8[g8] f4 r4 \bar "|" g4 e4 d4 \bar "|" c2 r4 \bar "|" d4 e4 f4 \bar "|" g4 f4 e4 \bar "|" f2. \bar ":|."
}

verseOne = \lyricmode {
  Paul of the des -- ert your sons im -- plore Aid as we carr -- y the Good News,
  Christ is the Savi -- or, Our sins he bore To all the earth, none re -- fused;
  Saint Paul our Fa -- ther and found -- er, We ask for cour -- age like yours
  To con -- fess Je -- sus, With all our heart, To be true God and our Lord!
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