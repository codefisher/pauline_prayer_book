\version "2.18.2"

#(set! paper-alist (cons '("boolet size" . (cons (* 5 in) (* 2.5 in))) paper-alist))

\paper {
   #(set-paper-size "boolet size")
   indent = 0\cm
   ragged-last = ##f
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
  ees8[f8] g4 g4 \bar "|" ees8 d8 ees2 \bar "|" g8[aes8] bes4 bes4 \bar "|" aes8 f8 g2 \bar "|" \break
  g8([aes8]) bes4 bes4 \bar "|" aes8 g8 aes2 \bar "|" \break
  f8([g8]) aes4 aes4 \bar "|" g8 f8 g2 \bar "|" g4 f4 d4 \bar "|" ees2. \bar "|."
}
verseOne = \lyricmode {
  Gens e -- re -- mit -- ti -- ca,
  Tur -- ba The -- ba -- i -- ca, 
  Sol -- ve si -- len -- ti -- um
  Et fac tri -- pu -- di -- um,
  Per Can -- ti -- ca.
}

\score {
  <<
    \new Voice = "one" {
    \clef treble 
    \key c \minor
      \musicOne
    }
    \new Lyrics \lyricsto "one" {
      <<
      { \verseOne }
      >>

    }
  >>
}