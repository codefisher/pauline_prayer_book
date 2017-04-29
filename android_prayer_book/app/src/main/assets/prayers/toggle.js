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

var currentMary = prefObject.get("season-mary", "mary-ordinary");
var angelusCurrent = prefObject.get("season-angelus", "angelus");

function setup() {
    var maryOrdinary = document.getElementById('mary-ordinary');
    var maryLent =  document.getElementById('mary-lent');
    if(currentMary == "mary-ordinary"){
        maryOrdinary.style.display = "block";
        maryLent.style.display = "none";
    } else {
        maryOrdinary.style.display = "none";
        maryLent.style.display = "block";
    }
    var reginaCaeli = document.getElementById('regina-caeli');
    var angelus =  document.getElementById('angelus');
    if(angelusCurrent == "angelus"){
        angelus.style.display = "block";
        reginaCaeli.style.display = "none";
    } else {
        angelus.style.display = "none";
        reginaCaeli.style.display = "block";
    }
}

function maryToggle() {
    if(currentMary == "mary-ordinary"){
        currentMary = "mary-lent";
    } else {
        currentMary = "mary-ordinary";
    }
    prefObject.set("season-mary", currentMary);
    setup();
}

function angelusToggle() {
    if(angelusCurrent == "angelus"){
        angelusCurrent = "regina-caeli";
    } else {
        angelusCurrent = "angelus";
    }
    prefObject.set("season-angelus", angelusCurrent);
    setup();
}
