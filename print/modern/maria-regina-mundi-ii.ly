\version "2.18.2"

#(set! paper-alist (cons '("boolet size" . (cons (* 5 in) (* 2.75 in))) paper-alist))

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
  \time 4/4
  d2 d4 c4 \bar "|" d2 f4 f4 \bar "|" e2( d4 cis4) \bar "|" d1 \bar "|" f2 g4 bes4 \bar "|" \break 
  d,4( cis4) bes4 f'4 \bar "|" g2 g2 \bar "|" a1 \bar "|" d2 bes4 a4 \bar "|" bes4( a4) g2 \bar "|" \break 
  d'2 bes4 a4 \bar "|" g4( a4) f2 \bar "|" c'4 c4 a2 \bar "|" c1 \bar "|" a4 a4 a2 \bar "|" d,1 \bar ":|." \break
}
verseOne = \lyricmode {
  Ma -- ri -- a Re -- gi -- na mun -- di. Ma -- ri -- a
  Ma -- ter Ec -- cle -- si -- ae Ti -- bi as -- su -- mus
  Tu -- i me -- mo -- res vi -- gi -- la -- mus! Vi -- gi -- la -- mus!
}


\score {
  <<
    \new Voice = "one" {
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