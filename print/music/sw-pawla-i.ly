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
  c8( [b8]) a8( [g8]) a8[ f8] \bar "|" e4 d4 c4\fermata \bar "|." \break
}
verseOne = \lyricmode {
  De -- cy -- ju -- sza  gniew się sro -- ży,
  By chreś -- cijań -- ską gu -- bić krew
}

verseTwo = \lyricmode {
  Pój -- dę tam gdzie bo -- ry si -- ne
  Sto -- ją ran -- kiem "w sre" -- brney mgle
  Jak "w płaszcz" "w ci" -- szę się o -- wi -- nę,
  Ich głąb mroczna skry -- je mnie.
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
	 A gdzież ci to słu -- go Bo -- ży?
	 Nu -- cić Pa -- nu wol -- ny śpiew?
      }

      >>
      \verseTwo
    }
  >>
}