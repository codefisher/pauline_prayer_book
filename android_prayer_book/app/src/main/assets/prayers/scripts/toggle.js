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

var currentMary = "mary-ordinary";
var angelusCurrent = "angelus";

function init() {
    var year = new Date().getFullYear();
    var date = getEaster(year);
    var month = date[0];
    var day = date[1];
    var easter = new Date(year, month-1, day);
    var ashWednesday = new Date(easter);
    ashWednesday.setDate(easter.getDate() - 46);
    var pentecost = new Date(easter);
    pentecost.setDate(easter.getDate() + 49);
    var today = new Date();
    if(today >= ashWednesday && today < easter){
        currentMary = "mary-lent";
    } else {
        currentMary = "mary-ordinary";
    }
    if(today >= easter && today <= pentecost){
        angelusCurrent = "regina-caeli";
    } else {
        angelusCurrent = "angelus";
    }
}

init();

function setDisplayAll(selector, mode) {
    var items = document.querySelectorAll(selector);
    for(var i = 0; i < items.length; i++) {
        if(mode == "none") {
            items[i].classList.add("togglehidden");
        } else {
            items[i].classList.remove("togglehidden");
        }
    }
}

function toggleSeason() {
    if(currentMary == "mary-ordinary"){
        setDisplayAll('#mary-ordinary', "block");
        setDisplayAll('#mary-lent', "none");
    } else {
        setDisplayAll('#mary-ordinary', "none");
        setDisplayAll('#mary-lent', "block");
    }
    if(angelusCurrent == "angelus"){
        setDisplayAll('#regina-caeli', "none");
        setDisplayAll('#angelus', "block");
    } else {
        setDisplayAll('#regina-caeli', "block");
        setDisplayAll('#angelus', "none");
    }
}

function maryToggle() {
    if(currentMary == "mary-ordinary"){
        currentMary = "mary-lent";
    } else {
        currentMary = "mary-ordinary";
    }
    prefObject.set("season-mary", currentMary);
    toggleSeason();
}

function angelusToggle() {
    if(angelusCurrent == "angelus"){
        angelusCurrent = "regina-caeli";
    } else {
        angelusCurrent = "angelus";
    }
    prefObject.set("season-angelus", angelusCurrent);
    toggleSeason();
}

var currentHymn = prefObject.get("paul-hymn", "hymn-1");

function setupHymn() {
    ["hymn-1", "hymn-2"].forEach(function(element) {
        var cong = document.querySelectorAll("#" + element + " .congregation");
        var width = 0;
        for(var i = 0; i < cong.length; i++){
            var w = parseInt(getComputedStyle(cong[i]).width.replace(/[a-z]/g, ''));
            if(w > width) {
                width = w;
            }
        }
        for(var i = 0; i < cong.length; i++){
            cong[i].style.width = width + "px";
        }
    });
    if(currentHymn == "hymn-1"){
        setDisplayAll('#hymn-1', "block");
        setDisplayAll('#hymn-2', "none");
    } else {
        setDisplayAll('#hymn-1', "none");
        setDisplayAll('#hymn-2', "block");
    }
}

function hymnToggle() {
    if(currentHymn == "hymn-1"){
        currentHymn = "hymn-2";
    } else {
        currentHymn = "hymn-1";
    }
    prefObject.set("paul-hymn", currentHymn);
    setupHymn();
}