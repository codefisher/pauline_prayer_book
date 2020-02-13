function loadNecrology() {
    var xmlhttp = new XMLHttpRequest();
    var url = "necrology.json";

    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status == 200 || this.status == 0)) { // Safari always gives 0
            var data = JSON.parse(this.responseText);
            loadTable(data);
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.overrideMimeType("application/json");
    xmlhttp.send();

}

function loadTable(data) {
    var currentDate = new Date();
    currentDate.setDate(currentDate.getDate() + 1);
    var day = currentDate.getDate()
    var month = currentDate.getMonth() + 1
    if(day < 10) {
        day = "0" + day;
    }
    if(month < 10) {
        month = "0" + month;
    }
    var key = month + "" + day;
    var info = data[key];
    if(!info || info.length == 0) {
        document.getElementById('necrology-not-found').style.display = "block";
    } else {
        var necrology = document.getElementById('necrology');

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
        necrology.style.display = "table";
    }
}