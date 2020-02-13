var TEMP = 140;
var MP3_PATH = "/mp3/";

if (typeof chantPlayer == "undefined") {
    // fall back if we are not in Android where prefObject
    // is gives access to application settings
    var chantPlayer = {
        play: function(songName) {
            // first try to call the ios version
            window.location = "musicplay://" + songName.replace("-", "_");
            // now what could work on the desktop
            var src = MP3_PATH + songName + ".mp3";
            var oldAudio = document.getElementById('audio-element');
            if(oldAudio != null) {
                oldAudio.pause();
                oldAudio.parentNode.removeChild(oldAudio);
            }
            var audio = document.createElement('audio');
            audio.id = "audio-element";
            audio.setAttribute('src', src);
            audio.setAttribute('type', 'audio/mpeg');
            document.body.appendChild(audio);
            audio.play();
        },
        stop: function() {
            // first try to call the ios version
            window.location = "musicplay:";
            // now what could work on the desktop
            var oldAudio = document.getElementById('audio-element');
            if(oldAudio) {
                oldAudio.pause();
                oldAudio.parentNode.removeChild(oldAudio);
            }
        }
    }
}

function stopSong(svgId, audioId) {
    chantPlayer.stop();
    var svgTarget = document.getElementById(svgId);
    var svgDoc = svgTarget.getSVGDocument();
    var oldCircle = svgDoc.getElementById("note-marker");
    if(oldCircle != null) {
        oldCircle.parentNode.removeChild(oldCircle);
    }
    document.getElementById(audioId + "-play").removeAttribute('disabled');
    document.getElementById(audioId + "-stop").setAttribute('disabled', 'disabled');
}

function playSong(svgId, audioId, url, mutiple) {
    document.getElementById(audioId + "-stop").removeAttribute('disabled');
    document.getElementById(audioId + "-play").setAttribute('disabled', 'disabled');

    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status == 200 || this.status == 0)) { // Safari always gives 0
            var pitches = JSON.parse(this.responseText);
            var svgTarget = document.getElementById(svgId);
            var notesNodes = [];

                var svgDoc = svgTarget.getSVGDocument();
                var oldCircle = svgDoc.getElementById("note-marker");
                if(oldCircle != null) {
                    oldCircle.parentNode.removeChild(oldCircle);
                }
                var circle = svgDoc.createElementNS('http://www.w3.org/2000/svg', 'circle');
                circle.setAttribute('r', '6');
                circle.setAttribute('cx', '6');
                circle.setAttribute('cy', '6');
                circle.id = "note-marker";
                circle.setAttribute('fill', '#ffaaaa');
                var top = svgDoc.getElementById('surface1');
                top.insertBefore(circle, top.childNodes[0]);

                var possibleNotes = svgDoc.querySelectorAll('use');

                for(var i = 0; i < possibleNotes.length; i++) {
                    var xlink = possibleNotes[i].getAttributeNS('http://www.w3.org/1999/xlink', 'href');
                    if(xlink) {
                        var glyph = xlink.split("#")[1];
                        var data = notes[glyph]
                        if(data) {
                            notesNodes.push(possibleNotes[i]);
                            possibleNotes[i].notes = notes[glyph]['count'];
                            if(notes[glyph]['notes']) {
                                possibleNotes[i].notePostions = notes[glyph]['notes'];
                            }
                        }
                    }
                }

                var i = 0;
                var j = 0;
                var multi_pos = 0;
                function duraction(l) {
                    var count = parseInt(notesNodes[l].notes);
                    var length = 0;
                    if(count == 0 && typeof mutiple != 'undefined') {
                        count = mutiple[multi_pos];
                        multi_pos++;
                    }
                    for(var k = j; k < j + count; k++){
                        length += pitches[k][1];
                    }
                    j += count;
                    return length * (60 / TEMP * 1000);
                }
                function highlight() {
                    if(circle.parentNode == null) {
                        // it got deleted out of the document because we started again
                        return;
                    }
                    var x = parseInt(notesNodes[i].getAttribute('x'));
                    var y = parseInt(notesNodes[i].getAttribute('y'));

                    var pos = notesNodes[i].notePostions;

                    function update(n) {
                        if(circle.parentNode == null) {
                            return;
                        }
                        if(n >= pos.length) {
                            return;
                        }
                        var notePos = pos[n];
                        circle.setAttribute('cx', x + notePos[0]);
                        circle.setAttribute('cy', y + notePos[1]);
                        if(n < pos.length && pitches[j + n] != null) {
                            setTimeout(function() {
                                update(n+1);
                            }, pitches[j + n][1] * (60 / TEMP * 1000));
                        }
                    }
                    update(0);

                    i++;
                    if(i < notesNodes.length) {
                        setTimeout(function() {
                            highlight(); 
                        }, duraction(i-1));
                    } else {
                        setTimeout(function() {
                            circle.parentNode.removeChild(circle);
                            stopSong(svgId, audioId)
                        }, duraction(i-1));
                    }
                }
                chantPlayer.play(audioId);
                highlight(); 
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.overrideMimeType("application/json");
    xmlhttp.send();
}
