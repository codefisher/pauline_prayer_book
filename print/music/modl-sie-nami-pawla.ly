\version "2.18.2"

#(set! paper-alist (cons '("boolet size" . (cons (* 6 in) (* 2.5 in))) paper-alist))

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
  \time 4/4
  a'\breve b8 a4 g8([a8]) c8[(a8) g8] \bar "|" a\breve \bar "" \break
   a8 a8 b8 a4(g4)
  a\breve a8 a4 g8([a8]) c8[(a8) g8] \bar "|" \break a\breve
  g8 a8 b8 a4(g4) \bar "|."
}

l=\once \override LyricText #'self-alignment-X = #-1 

verseOne = \lyricmode {
  \l "Módl się za" na -- mi, _ _ \l "święty nasz Ojcze Pawle Pierwszy" Pu -- stel -- ni -- ku
  \l "Abyśmy się" sta -- li, _ _ \l "godnymi obietnic"
  Chry -- stu -- so -- wych.
}

\score {
  <<
    \new Voice = "one" {
    \clef treble 
    \override Staff.TimeSignature #'stencil = ##f 
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