var currentMary = prefObject.get("season-mary", "mary-ordinary");
var angelusCurrent = prefObject.get("season-angelus", "angelus");
alert(angelusCurrent);

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