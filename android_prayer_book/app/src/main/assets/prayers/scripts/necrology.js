var data = {};

function setupNecrology(locale) {
    loadNecrology();
    $( function() {
    alert($.datepicker.regional.it);
        $.datepicker.setDefaults($.datepicker.regional[locale]);
        $("#day").datepicker({
            changeMonth: true, dateFormat: "dd/mm",
            onSelect: function(dateText, inst) {
                var date = dateText.split("/");
                loadTableForDate(date[1], date[0]);
            }
        });
    } );
    document.getElementById('day').addEventListener("change", function(event) {
        var date = event.target.value.split("/");
        loadTableForDate(date[1], date[0]);
    });
}

function loadNecrology() {
    var xmlhttp = new XMLHttpRequest();
    var url = "necrology.json";

    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status == 200 || this.status == 0)) { // Safari always gives 0
            data = JSON.parse(this.responseText);
            loadTable();
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.overrideMimeType("application/json");
    xmlhttp.send();

}

function loadTable() {
    loadTableInc(1)
}

function loadTableInc(days) {
    var currentDate = new Date();
    loadTableHelper(days, currentDate)
}

function previous() {
    var date = document.getElementById('day').value.split("/");
    var currentDate = new Date(new Date().getFullYear(), date[1] - 1, date[0]);
    loadTableHelper(-1, currentDate)
}

function next() {
    var date = document.getElementById('day').value.split("/");
    var currentDate = new Date(new Date().getFullYear(), date[1] - 1, date[0]);
    loadTableHelper(1, currentDate)
}

function loadTableHelper(days, currentDate) {
    currentDate.setDate(currentDate.getDate() + days);
    var day = currentDate.getDate()
    var month = currentDate.getMonth() + 1
    if(day < 10) {
        day = "0" + day;
    }
    if(month < 10) {
        month = "0" + month;
    }
    loadTableForDate(month, day);
    var dateBox = document.getElementById('day');
    if(dateBox) {
        dateBox.value = day + "/" + month;
    }
}

function loadTableForDate(month, day) {
    var key = month + "" + day;
    var info = data[key];
    var notFound = document.getElementById('necrology-not-found');
    var necrology = document.getElementById('necrology');
    if(!info || info.length == 0) {
        notFound.style.display = "block";
        necrology.style.display = "none";
    } else {
        while(necrology.firstChild) {
            necrology.removeChild(necrology.firstChild)
        }
        for(var i = 0; i < info.length; i++){
            var row = document.createElement('tr');
            var name = document.createElement('td');
            name.textContent = info[i]['name'];
            row.appendChild(name);
            var description = document.createElement('td');
            description.textContent = info[i]['description'];
            row.appendChild(description);
            necrology.appendChild(row);
        }
        notFound.style.display = "none";
        necrology.style.display = "table";
    }
}