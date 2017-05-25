\version "2.18.2"

#(set! paper-alist (cons '("boolet size" . (cons (* 6 in) (* 3.5 in))) paper-alist))

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
  g'4 bes4. aes8 \bar "|" aes4 g4 r4 \bar "|" f8 g8 aes4. d8 \bar "|" f,4 ees4 r4 \bar "|" \break
  ees4 d4. ees8 \bar "|" c'2 c4 \bar "|" c8 ees8 d4. c8 \bar "|" c4 bes4 r4 \bar "|" \break
  \bar ".|:" bes4 bes4 bes4 \bar "|" d8[c8] bes4 r4 \bar "|" bes8 bes8 c4 d4 \bar "|" ees4 g,4 r4 \bar "|"  \break
  g4 aes4. bes8 \bar "|" bes4 g4 r4 \bar "|" f8 c'8 bes4. d,8 \bar "|" f4 ees4 r4 \bar "|." 
}


verseOne = \lyricmode {
  Przy -- bądź o du -- szo spra -- gnio -- na po -- ko -- ju,
  Pod ro -- zło -- ży -- stej mej pal -- my ko -- na -- ry,
  spocz -- nij "w jej" cie -- niu po u -- pal -- nym zno -- ju,
  tu na ka -- mie -- niu u skal -- nej pie -- cza -- ry.
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