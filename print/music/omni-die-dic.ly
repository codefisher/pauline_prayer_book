\version "2.18.2"

#(set! paper-alist (cons '("boolet size" . (cons (* 5 in) (* 6.25 in))) paper-alist))

\paper {
   #(set-paper-size "boolet size")
   indent = 0\cm
   ragged-last = ##t
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

  d4 c8 d8 f4 \bar "'" g8 f8 e8 d4 \bar "'" f8 g8 a8 a8 g8 f8 a4 \halfAddBar \break
  e8 f8 g8 e4 \bar "'" d8 c8 e8 e4 \bar "'" d8 f8 a8 g8 f8 e8 d4 \bar "|." \break
  d8 a'8 a8 g4 \bar "'" a8 f8 g8 e4 \bar "'" f8 e8 d8 a'8 f8 g8 a4 \halfAddBar \break
  a8 c8 d8 a4 \bar "'" g8 e8 a8 a4 \bar "'" e8 f8 g8 d8 f8 e8 d4 \bar "|." \break
  f8 e8 g8 d4 \bar "'" f8 e8 d8 c8 \bar "'" f8 g8 a8 g8 c8 b8 a4 \halfAddBar \break
  d8 c8 a8 f4 \bar "'" g8 a8 a8 d,4 \bar "'" d8 c8 e8 e8 d8 c8 d4 \bar "|." \break
  d8[e8 d8] c8(d8) \bar "|." \break
  
}
verseOne = \lyricmode {
  "1. Om" -- ni di -- e dic Ma -- ri -- ae me -- a lau -- des a -- ni -- ma: 
  E -- jus fe -- sta, e -- jus ge -- sta co -- le de -- vo -- tis -- si -- ma.
  "3. Ip" -- sam co -- le, ut de mo -- le cri -- mi  -- num te li -- be -- ret:
  Hanc ap -- pel -- la, ne pro -- cel -- la vi -- ti -- or -- um su -- pe -- ret.
  "5. Cle" -- mens au -- di, tu -- ae lau -- di quos in -- stan -- tes con -- spi -- cis: 
  Mun -- da re -- os, et fac e -- os Do -- nis dig -- nos coe -- li -- cis. 
  A -- men.
}


\score {
  <<
    \new Voice = "one" {
    \clef treble 
    \override Staff.TimeSignature #'stencil = ##f 
    \key c \major
      \musicOne
    }
    \new Lyrics \lyricsto "one" {
      <<
      { \verseOne }
      \new Lyrics {
	\set associatedVoice = "one"
	 "2. Con" -- tem -- pla -- re et mi -- ra -- re E -- jus cel -- si -- tu -- di -- nem,
         Dic fe -- li -- cem ge -- ni -- tri -- cem, Dic be -- a -- tam Vir -- gi -- nem.
         "4. Prop" -- ter he -- vam ho -- mo sae -- vam ac -- ce -- pit sen -- ten -- ti -- am;
         Per Ma -- ri -- am ha -- bet vi -- am, quae du -- cit ad pa -- tri -- am. 
         "6. Vir" -- ga Jes -- se, spes op -- pres -- sae men -- tis et re -- fu -- gi -- um; 
         De -- cus mun -- di, lux pro -- fun -- di, Do -- mi -- ni sac -- ra -- ri -- um.
      }

      >>
    }
  >>
}