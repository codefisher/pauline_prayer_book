\version "2.18.2"

#(set! paper-alist (cons '("boolet size" . (cons (* 6 in) (* 3.5 in))) paper-alist))

\paper {
   #(set-paper-size "boolet size")
   indent = 0\cm
   ragged-last = ##t
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
  \time 6/8
  e8 \bar "|" g4 g8 a4 e8 \bar "|" g4. f4 e8 \bar "|" f4 \bar "" \break
  a8 g4 d8 e4.(e4) \bar "|" \break
  \bar ".|:" g8 \bar "|" c4 c8 d4 c8 \bar "|" b4. a4 a8 \bar "|" g4 g8 f4 d8 \bar "|" \break 
  \set Score.repeatCommands = #'((volta "1."))
  g4.(g4) \bar "|" 
  \set Score.repeatCommands = #'((volta #f) (volta "2."))
  g4.(g4) 
  \set Score.repeatCommands = #(list '(volta #f) 'end-repeat)
  \bar "|."
}


verseOne = \lyricmode {
  Jak ma -- my iść do Bo -- ga "w tych" ci -- chych bło -- gich dniach,
  wska -- za -- na jest name dro -- ga na no -- wi -- cja -- tu drzwiach drzwich
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
      >>
    }
  >>
  \layout {}
  \midi {}
}