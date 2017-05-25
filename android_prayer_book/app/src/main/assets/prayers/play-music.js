var TEMP = 140;

function documentPositionComparator (a, b) {
    if (a === b) {
        return 0;
    }
    var position = a.compareDocumentPosition(b);
    if (position & Node.DOCUMENT_POSITION_FOLLOWING 
            || position & Node.DOCUMENT_POSITION_CONTAINED_BY) {
        return -1;
    } else if (position & Node.DOCUMENT_POSITION_PRECEDING 
            || position & Node.DOCUMENT_POSITION_CONTAINS) {
        return 1;
    } else {
        return 0;
    }
}

function playSong(svgId, audioId, url, mutiple) {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status == 200 || this.status == 0)) { // Safari always gives 0

            var pitches = JSON.parse(this.responseText);
            var svgTarget = document.getElementById(svgId);
            var notesNodes = [];

                var svgDoc = svgTarget.getSVGDocument();
                var circle = svgDoc.createElementNS('http://www.w3.org/2000/svg', 'circle');
                circle.setAttribute('r', '6');
                circle.setAttribute('cx', '6');
                circle.setAttribute('cy', '6');
                circle.setAttribute('fill', '#ffaaaa');
                var top = svgDoc.getElementById('surface1');
                top.insertBefore(circle, top.childNodes[0]);

                for(var i = 0; i < notes.length; i++) {
                    var glyphs = svgDoc.querySelectorAll(notes[i]["path"])
                        if(glyphs.length != 0) {
                        var glyph = glyphs[0].parentNode.id;
                        var nodes = svgDoc.querySelectorAll('[*|href="#' + glyph + '"]');
                        for(var j = 0; j < nodes.length; j++) {
                            notesNodes.push(nodes[j]);
                            nodes[j].notes = notes[i]['count'];
                            if(notes[i]['notes']) {
                                nodes[j].notePostions = notes[i]['notes'];
                            }
                            //nodes[j].parentNode.innerNote = nodes[j]
                        }
                    }
                }

                notesNodes.sort(documentPositionComparator);
                var i = 0;
                var j = 0;
                var multi_pos = 0;
                function duraction(l) {
                    var count = parseInt(notesNodes[l].notes);
                    var length = 0;
                    if(count == 0) {
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
                    var bBox = notesNodes[i].getBBox();
                    var x = parseInt(notesNodes[i].getAttribute('x'));
                    var y = parseInt(notesNodes[i].getAttribute('y'));
                    if(notesNodes[i].notePostions == null) {
                        circle.setAttribute('cx', x + bBox.width *  0.5);
                        circle.setAttribute('cy', y);
                    } else {
                        var pos = notesNodes[i].notePostions;
                        
                        function update(n) {
                            if(n >= pos.length) {
                                return;
                            }
                            var notePos = pos[n];
                            circle.setAttribute('cx', x + bBox.width * notePos[0]);
                            circle.setAttribute('cy', y - (bBox.height * notePos[1]));
                            if(n < pos.length && pitches[j + n] != null) {
                                setTimeout(function() {
                                    update(n+1); 
                                }, pitches[j + n][1] * (60 / TEMP * 1000));
                            }
                        }
                        update(0);
                    }
                    i++;
                    if(i < notesNodes.length) {
                        setTimeout(function() {
                            highlight(); 
                        }, duraction(i-1));
                    } else {
                        setTimeout(function() {
                            circle.parentNode.removeChild(circle);
                        }, duraction(i-1));
                    }
                }
                try {
                    chantPlayer.play(audioId);
                } catch(e) {
                    document.getElementById(audioId).play();
                }
                highlight(); 
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.overrideMimeType("application/json");
    xmlhttp.send();
}
