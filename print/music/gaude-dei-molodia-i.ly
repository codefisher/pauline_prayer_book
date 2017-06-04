\version "2.18.2"

#(set! paper-alist (cons '("boolet size" . (cons (* 5 in) (* 6.5 in))) paper-alist))

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

halfBar = \once \override Staff.BarLine #'bar-extent = #'(-1.5 . 1.5) 
halfAddBar = { \halfBar \bar "|" }

musicOne = \relative c' {
  \autoBeamOff
  \cadenzaOn
  
  d8 e8[ g8] g8 g8[ fis8] d8[ fis8] d8[ e8] e8 \bar "'" e8[ g8] g8 fis8[ g8] a8[ g8] e8[ fis8] fis8 fis4 \halfAddBar \break
  fis8[ g8 a8] a4 g4 \bar "'" fis8[ d8] g8 fis8 e8 fis8[ g8] a8 a8 a8[ g8] a8 a8[ b8 a8] fis4 fis4 \bar "|" \break
  r8 e8[ b'8 c8] \once \stemUp  b4 \bar "'" b8[ a8] b8[ c!8] b8[ a8] \once \stemUp b8 a4 \halfAddBar a8 a8 g8 g8[ fis8] e8[ fis8] e8[ d8] \bar "" \break
  e8 e8[ fis8] fis4 fis4 \bar "|" r8 g8 fis8[ e8] g8 fis4 \bar "'" e8 d8 e8[ g8] g8 \bar "" \break
  fis8 g8 a8[ b8] b8 b8[ a8 b8] fis4 fis4 \halfAddBar e8( \once \stemUp b'4^\marcato  a8) b8[ c8] \stemUp b8 b8 b8 \stemNeutral \bar "" \break
  b8[ a8] \once \stemUp b8 a8 a8 a8[ b8] a8 a8 g8[ fis8] e8[ fis8] fis8[ g8] fis4^( e4) \halfAddBar \break
  e8[ a8] a8[ g8] a8 a8[ b8 a8] fis4 fis4 \halfAddBar d8 e8[ g8] g8 a8[ fis8] e8[ fis8] e8 d4 \halfAddBar \break
  d8[ e8] fis8 g8 a8[ g8] a8 a8[ b8 a8] fis4 fis4 \bar "|." 
  
}
verseOne = \lyricmode {
  Gau -- de De -- i Ge -- ni -- trix, Vir -- go im -- ma -- cu -- la -- ta;
  Gau -- de, _ quae gau -- di -- um ab An -- ge -- lo su -- sce -- pis -- ti
  Gau -- de, quae ge -- nu -- is  -- ti ae -- ter -- ni lu -- mi -- nis
  cla -- ri -- ta -- tem; Gau -- de Ma -- ter, gau -- de san -- cta
  De -- i Ge -- ni -- trix Vir -- go; tu so -- la Ma -- ter
  in -- nu -- pta;  te lau -- dat om -- nis fa -- ctu -- ra, 
  Ge -- ni -- tri -- cem lu -- cis; sis pro no -- bis quae -- sum -- us,
  per -- pe -- tu -- a In -- ter -- ven -- trix.
}

\score {
  <<
    \new Voice = "one" {
    \clef treble 
    \override Staff.TimeSignature #'stencil = ##f 
    \key d \major
      \musicOne
    }
    \new Lyrics \lyricsto "one" {
      \verseOne
    }
  >>
}
