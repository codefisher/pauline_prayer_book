\version "2.18.2"

#(set! paper-alist (cons '("boolet size" . (cons (* 5 in) (* 5.25 in))) paper-alist))

\paper {
   #(set-paper-size "boolet size")
   indent = 0\cm
   top-margin = 0
   bottom-margin = 0
   right-margin = 0
   left-margin = 0
} 

\header {
  tagline = ""  % removed
}

musicOne = \relative c' {
  \autoBeamOff
  \cadenzaOn
  \time 3/4
  c8 e8 g4 g4 \bar "|" e8 c8 a'4 g4 \bar "|" \break
  g8 g8 f4 e4 \bar "|" g8 e8 d2 \bar ":|." \break
  d8 e8 f4 f4 \bar "|" e8 d8 e8( [f8]) g4\fermata \bar "|" \break
  f8 g8 a8 a8( [b8]) \bar "|" c8[ b8] a4 g4\fermata \bar "|" \break
  d8 e8 f4 f4  \bar "|" e8 d8 d8( [f8]) g4\fermata \bar "|" \break
  c8( [b8]) a8( [g8]) a8 f8 \bar "|" e4 d4 c4\fermata \bar "|." \break
}
verseOne = \lyricmode {
  De -- ci -- a -- na Ter -- ret Mul -- tum
  Sae -- va per -- se -- cu -- ti -- o,
}

verseTwo = \lyricmode {
  Hinc pe -- ric -- la dec -- lin -- a -- bo
  E -- lon -- gan -- do fu -- gi -- ens,
  Ac in sil -- vis la -- ti -- ta -- bo
  So -- li De -- o ser -- vi -- ens.
}

\score {
  <<
    \new Voice = "one" {
    \clef treble 
    \key c \major
      \musicOne
    }
    \new Lyrics \lyricsto "one" {
      <<
      { \verseOne }
      \new Lyrics {
	\set associatedVoice = "one"
	 Li -- be -- rum -- que de -- i cul -- tum
	 to -- ta men -- te cu -- pi -- o,
      }

      >>
      \verseTwo
    }
  >>
}