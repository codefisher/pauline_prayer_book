var jsonData = {};
var year = null;

function loadCalendar() {
    loadHelper(publishCalendar);
}

function setupFront() {
    loadHelper(publishFront);
}

function todayFeast() {
    loadHelper(publishToday);
}

function loadHelper(func) {
    var xmlhttp = new XMLHttpRequest();
    var url = "feasts.json";

    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status == 200 || this.status == 0)) { // Safari always gives 0
            jsonData = JSON.parse(this.responseText);
            func();
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.overrideMimeType("application/json");
    xmlhttp.send();
}

function formatDate(currentDate) {
    var day = currentDate.getDate()
    var month = currentDate.getMonth() + 1
    if(day < 10) {
        day = "0" + day;
    }
    if(month < 10) {
        month = "0" + month;
    }
    return month + "" + day;
}

function publishCalendar() {
    var today = new Date();
    year = today.getFullYear();
    publishCalendarHelper(year);
}

function next() {
    year += 1;
    publishCalendarHelper(year);
}

function previous() {
    year -= 1;
    publishCalendarHelper(year);
}

function computeCalendar(jsonData, displayYear) {
    var data = Object.assign({}, jsonData);
    var date = getEaster(displayYear);
    var easter = new Date(displayYear, date[0]-1, date[1]);
    var motherChurch = new Date(easter);
    motherChurch.setDate(easter.getDate() + 50);
    data[formatDate(motherChurch)] = data["mother-church"];

    var stPaul = new Date(displayYear, 0, 15);
    if(stPaul.getDay()) {
        var diff = 7 - stPaul.getDay();
        var external = new Date(stPaul);
        external.setDate(external.getDate() + diff);
        data[formatDate(external)] = data["paul-external"];

        var novena = new Date(external);
        novena.setDate(novena.getDate() - 9);
        data[formatDate(novena)] = data["paul-novena"];
    } else {
        var novena = new Date(stPaul);
        novena.setDate(novena.getDate() - 9);
        data[formatDate(novena)] = data["paul-novena"];
    }

    var last = new Date(displayYear, 9, 31);
    if(last.getDay()) {
        var diff = last.getDay();
        last.setDate(last.getDate() - diff);
    }
    data[formatDate(last)] = data["church-consecration"];
    return data;
}

function publishCalendarHelper(displayYear) {
    document.getElementById('year').innerHTML = displayYear;

    var data = computeCalendar(jsonData, displayYear)

    var keys = Object.keys(data).sort();

    var currentList = null;
    var currentMonth = null;
    var datesBox = document.getElementById("dates");

    while(datesBox.firstChild) {
        datesBox.removeChild(datesBox.firstChild);
    }

    for (const key of keys){
        if(key.length == 4) {
            var dateValue = data[key];
            var feastDate = new Date(displayYear, key.slice(0, 2) - 1, key.slice(2,4));
            var month = feastDate.toLocaleString(document.body.getAttribute("lang"), { month: 'long' });
            if(month != currentMonth) {
                var heading = document.createElement("h2");
                var textnode = document.createTextNode(month);
                heading.appendChild(textnode);
                datesBox.appendChild(heading);
                currentMonth = month;
                currentList = document.createElement("ol");
                datesBox.appendChild(currentList);
            }
            var item = heading = document.createElement("li");
            item.setAttribute('value', feastDate.getDate());
            createDateEntry(dateValue, item);
            currentList.appendChild(item);
        }
    }
}

function createDateEntry(dateValue, item) {
    if(dateValue["day"]) {
        var day = heading = document.createElement("em");
        var textnode = document.createTextNode(dateValue["day"] + " ");
        day.appendChild(textnode);
        item.appendChild(day);
    }
    if(dateValue["link"]) {
        var name = heading = document.createElement("a");
        var textnode = document.createTextNode(dateValue["name"]);
        name.appendChild(textnode);
        name.setAttribute('href', dateValue["link"]);
        item.appendChild(name);
    } else {
        var name = heading = document.createElement("span");
        var textnode = document.createTextNode(dateValue["name"]);
        name.appendChild(textnode);
        item.appendChild(name);
    }
    if(dateValue["type"]) {
        var feastType = heading = document.createElement("span");
        var textnode = document.createTextNode(" " + dateValue["type"]);
        feastType.appendChild(textnode);
        feastType.setAttribute('class', "feast-type");
        item.appendChild(feastType);
    }
}

function setDisplayAll(selector, mode) {
    var items = document.querySelectorAll(selector);
    for(var i = 0; i < items.length; i++) {
        items[i].style.display = mode;
    }
}

function publishToday() {
    var today = new Date();
    var data = computeCalendar(jsonData, today.getFullYear());
    var existsToday = addFeastToBox(data, today, "today-feast-box");
    setDisplayAll('#today', existsToday ? "block" : "none");
}

function publishFront() {
    var today = new Date();
    var tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);
    var data = computeCalendar(jsonData, today.getFullYear());

    var day = today.getDay();

    if(day) {
        var litany = data["litany"][day - 1];
        var box = document.getElementById('litany-box');
        for(var i = 0; i < litany.length; i++) {
            if(i) {
                var textnode = document.createTextNode(" or ");
                box.appendChild(textnode);
            }
            if(litany[i]["link"]) {
                var name = heading = document.createElement("a");
                name.setAttribute('href', litany[i]["link"]);
            } else {
                var name = heading = document.createElement("span");
            }
            var textnode = document.createTextNode(litany[i]["name"]);
            name.appendChild(textnode);
            box.appendChild(name);
        }
        setDisplayAll('#today', "block");
    } else {
        setDisplayAll('#litany', "none");
    }

    var existsToday = addFeastToBox(data, today, "today-feast-box");
    if(!existsToday) {
        setDisplayAll('#today-feast', "none");
        setDisplayAll('#today', day ? "block" : "none");
    }

    var existsTomorrow = addFeastToBox(data, tomorrow, "tomorrow-feast-box");
    setDisplayAll('#tomorrow', existsTomorrow ? "block" : "none");
}

function addFeastToBox(data, day, box) {
    var dateValue = data[formatDate(day)];
    if(dateValue) {
        var container = document.getElementById(box);
        createDateEntry(dateValue, container)
        return true;
    }
    return false;
}