\version "2.18.2"

#(set! paper-alist (cons '("boolet size" . (cons (* 6 in) (* 4 in))) paper-alist))

\paper {
   #(set-paper-size "boolet size")
   indent = 0\cm
   ragged-last = ##f
   top-margin = 0
   bottom-margin = 0
   right-margin = 0
   left-margin = 0
} 

halfBar = \once \override Staff.BarLine #'bar-extent = #'(-1.5 . 1.5) 
halfAddBar = { \halfBar \bar "|" }

\header {
  tagline = ""  % removed
}

musicOne = \relative c' {
  \autoBeamOff
  \cadenzaOn
  \time 4/4
  bes'8[a8 g8 a8 bes8] bes4. \bar "|" g8 a8 a\breve \bar "" \break
  a\breve a8 bes8 bes4 \bar "" \break
  g8 a8 a8 a8 a8 bes8 a8 g8 a8 a8 a\breve \bar "" \break
  a\breve bes8 bes4 \halfAddBar g8 a\breve \bar "" \break
  a8 bes8 a8 g8 a8[bes8] bes4. \bar "|" a\breve a8 g8 a8 bes8 a4 g4 \bar "|" a8. bes8 \bar "|."
}

l=\once \override LyricText #'self-alignment-X = #-1 

verseOne = \lyricmode {
  "Módl - my" się: Bo -- źe, \l "który spawiłeś, że"
  \l "święty Paweł nasz Ojciec na pustyni świętość" o -- sią -- gnął
  spraw przez Je -- go przy -- czy -- nę a -- byś -- my \l "rozwijając w sobie"
  \l "ducha modlitwy i" służ -- by zbli -- "żali się"
  "w mi" -- łoś -- ci do Chie -- bie. \l "Przez Chrystusa" Pa -- na na -- sze -- go. _ A -- men.
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