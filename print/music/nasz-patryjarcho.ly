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
  \time 3/2
  fis2 fis2 fis2 \bar "|" a2 e2 e4(fis4) \bar "|" g4(a4) g2 fis2 \bar "|" fis2 e2 r2 \bar "|" \break
  b'2 b2 cis2 \bar "|" d2(a2) a4(b4) \bar "|" cis4 d4 cis2 b2 \bar "|" b2 a2 r2 \bar "|" a2 g2 a2 \bar "|" b1 b2 \bar "|" \break
  b4 b4 ais2 b2 \bar "|" cis1 cis2 \bar "|" d2 cis2 b2 \bar "|" ais1 g2 \bar "|" \break
  fis4 fis4 b2 ais2 \bar "|" cis2\fermata b2 r2 \bar "|." 
}


verseOne = \lyricmode {
  Nasz Pat -- ry -- jar -- cho, Pu -- ste -- lni -- ków wzo -- rze,
  Pua -- liń -- skie -- _ go Pra -- oj -- cze za -- ko -- nu, cześć Ci skła -- da -- my
  "w naj" -- głę -- bszej po -- ko -- rze, pro -- sząc o wspar -- cie
  u Bo -- że -- go Tro -- nu.
}


\score {
  <<
    \new Voice = "one" {
      \clef treble 
      \key d \major
      \musicOne
    }
    \new Lyrics \lyricsto "one" {
      <<
      { \verseOne }
      >>
    }
  >>
}