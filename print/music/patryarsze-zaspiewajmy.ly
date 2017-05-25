\version "2.18.2"

#(set! paper-alist (cons '("boolet size" . (cons (* 6 in) (* 2.75 in))) paper-alist))

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
  \partial 2
  \time 3/2
  <<
    \new Voice ="one" {
      \voiceOne
  a'2. a4 g4 f4 \bar "|" e4 f4 g2 c,2 \bar "|" bes'2. bes4 a4 g4 \bar "|" \break
  f4 g4 a2 f2 \bar ".|:" c'4. c8 bes4 a4 bes4 a4 \bar "|" bes4 c4 d2 s2 \bar "|" \break
  c4. a8 c4 c4 b4 e,4 \bar "|" g2 f2 s2 \bar "|."
    }
     \new Voice {
      \voiceTwo
      f2. f4 e4 d4 \bar "|" e4 d4 e2 s2 \bar "|" g2. g4 f4 e4 \bar "|" \break
      d4 e4 f2 f2 \bar ".|:" a4. a8 g4 f4 g4 f4 \bar "|" g4 a4 f2 r2 \bar "|" \break
      a4. f8 a4 a4 g4 c,4 \bar "|" e2 f2 r2 \bar "|."
     }
  >>
}


verseOne = \lyricmode {
  Pa -- try -- ar -- sze zaś -- pie -- waj -- my, Oj -- cu swe -- mu
  hołd od -- daj -- my czy -- stym ser -- cem, kor -- nym czo _ -- łem
  zgo -- dnym gło -- sem wszy -- scy spo -- łem.
}


\score {
  <<
    \new Voice {
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