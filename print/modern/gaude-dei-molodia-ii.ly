\version "2.18.2"

#(set! paper-alist (cons '("boolet size" . (cons (* 5.25 in) (* 9.25 in))) paper-alist))

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

halfBar = \once \override Staff.BarLine #'bar-extent = #'(-1.5 . 1.5) 
halfAddBar = { \halfBar \bar "|" }

musicOne = \relative c' {
  \autoBeamOff
  \cadenzaOn
  \time 4/4
  g'8 f8( g8) \bar "|" e8[ f8 g8] a8 \halfAddBar b8 c8[ b8 a8] b8( b8) \bar "|" \break
  b8 b8( [c8]) \halfAddBar b8 b8([a8 g8]) a8 g8( [f8] e8) e8 \bar "|" g8 f8( [g8]) e8( [f8]) \bar "|" \break
  g8( [a8]) g8( [a8 g8]) f8 g8 \halfAddBar g8( [a8 b8]) c8 c8 \halfAddBar c8 b8( b8[ a8]) g8( [b8 g8]) g8 \halfAddBar \break
  g8 a8( [b8]) c8 c8( [b8]) c8([d8 c8]) c8([b8]) a8([ b8]) d8 d8(d8) c8 c8 \bar "|" \break
  b8([c8]) b8 a8([b8]) \halfAddBar g8( [a8 b8]) a8([g8]) g8([f8]) e8 e8 \bar "|" g8 f8 e8 a8([b8]) \halfAddBar \break
  c8([d8 e8] d8[c8 b8]) b8 b8 c8([d8] e8) e8 \halfAddBar e8(d8)\( d8\)(c8) \halfAddBar c8([d8]) c8 b8 b8 \halfAddBar e8 d8([e8]) c8 c8 \bar "|" \break 
  b8([c8 b8]) a8 \halfAddBar b8 \bar "'" c8 b8([a8 g8]) g8 g8 f8[b8] a8 g8[f8] e8 \bar "|" \break
  b'8([a8]) c4 d8[e8 d8] c8 b8 b8 \bar "'" b8 c8 d8 \bar "|" c8[ b8 a8 g8] g8 \bar "|" \break
  b8 \bar "'" c8 \bar "'" d8[c8 d8] c8 d8 d8[e8 d8] c8[d8 c8] b8 b8 b8[c8 d8] c8 b8(a8) g8 g8  \halfAddBar \break
  b8([c8]) a8 f8([g8 f8]) e8 e8 \halfAddBar b'8[d8] c8[b8 a8] g8 g8 b8 a8([g8]) g8[f8] e8 e8 \bar "|" \break
  f8([a8]) g8[f8 e8] e8 e8 \halfAddBar f8([a8]) g8[f8 e8] e8 e8 \bar "|."
}
verseOne = \lyricmode {
  Gau -- de de -- i Ge -- ni -- trix
  Vir -- go im -- ma -- cu -- la -- ta Gau -- de quae
  ab an -- ge -- lo gau -- di -- um sus -- ce -- pi -- sti
  gau -- de quae ge -- nu -- is -- ti ae -- ter _ -- ni
  lu -- mi -- nis cla -- ri _ -- ta -- tem gau -- de ma -- ter
  gau -- de san _ -- cta De -- i Ge -- ni -- trix _  tu so -- la _
  ma -- ter es in tac -- ta. Te lau -- dat om -- nis
  cre -- a -- tu -- _  _ ra ge -- ni -- trix  lu -- cis
  sis pro no _ -- bis, quae _  -- su -- mus per _ -- pe -- tu -- a
  in _ -- ter -- ven -- trix ad Do -- mi -- num Je -- sum Chris _ -- tum
  al -- le -- lu -- ia al -- le -- lu -- ia
}

\score {
  <<
    \new Voice = "one" {
    \clef treble 
    \key c \major
      \musicOne
    }
    \new Lyrics \lyricsto "one" {
      \verseOne
    }
  >>
}
