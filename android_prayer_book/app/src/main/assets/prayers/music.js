if (typeof prefObject == "undefined") {
    // fall back if we are not in Android where prefObject 
    // is gives access to application settings
    var prefObject = {
        set: function(cname, cvalue) {
            var d = new Date();
            var exdays = 356 * 25;
            d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
            var expires = "expires="+d.toUTCString();
            document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
        },

        get: function(cname, def) {
            var name = cname + "=";
            var ca = document.cookie.split(';');
            for(var i = 0; i < ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0) == ' ') {
                    c = c.substring(1);
                }
                if (c.indexOf(name) == 0) {
                    return c.substring(name.length, c.length);
                }
            }
            return def;
        }
    }
}

var currentMusic = prefObject.get("music-notation", "modern-notation");

function setupMusic() {
    var gregorian = document.getElementsByClassName('gregorian-notation');
    var modern = document.getElementsByClassName('modern-notation');
    if(currentMusic == "modern-notation"){
        for(var i = 0; i < gregorian.length; i++) {
            gregorian[i].style.display = 'none';
        }
        for(var i = 0; i < modern.length; i++) {
            modern[i].style.display = 'block';
        }
    } else {
        for(var i = 0; i < gregorian.length; i++) {
            gregorian[i].style.display = 'block';
        }
        for(var i = 0; i < modern.length; i++) {
            modern[i].style.display = 'none';
        }
    }
}

function musicToggle() {
    if(currentMusic == "modern-notation"){
        currentMusic = "gregorian-notation";
    } else {
        currentMusic = "modern-notation";
    }
    prefObject.set("music-notation", currentMusic);
    setupMusic();
}