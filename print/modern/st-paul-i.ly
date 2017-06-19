\version "2.18.2"

#(set! paper-alist (cons '("boolet size" . (cons (* 5 in) (* 5 in))) paper-alist))

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
  From the Chris -- tian per -- se -- cu -- tion
  in the reign of De -- ci -- us,
}

verseTwo = \lyricmode {
  Thus with -- draw -- ing and re -- treat -- ing,
  he es -- caped the plight well -- known,
  there -- in hid -- den in the for -- est,
  he served only God a -- lone.
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
	 With no free -- dom to ad -- ore God,
         all his mind vi -- va -- ci -- ous
      }

      >>
      \verseTwo
    }
  >>
}