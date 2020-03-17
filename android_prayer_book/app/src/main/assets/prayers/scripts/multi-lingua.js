var languageNames = {
    "en": "English",
    "pl": "Polski",
    "de": "Deutsch",
    "hr": "Hrvatski",
    "it": "Italiano",
    "sk": "Slovenský",
    "la": "Latina"
};

var currentLang = "";
var menuList = null;
var current = null;
var box = null;
var langTable = null;

var status = null;

var originalDom = [];

function loadLanguage(langs) {
    var body = document.body;
    for(var i = 0; i < document.body.childNodes.length; i++) {
        var node = document.body.childNodes[i];
        if(node.nodeValue == null || node.nodeValue.trim().length != 0 && node.nodeType != Node.COMMENT_NODE) {
            originalDom.push(node);
        }
    }
    currentLang = body.getAttribute('lang');
    box = document.createElement("div");
    current = document.createElement("div");
    current.setAttribute('id', 'lang-current');
    var textnode = document.createTextNode(languageNames[currentLang]);
    current.addEventListener('click', function(event) {
        event.stopPropagation();
        menuList.style.display = "block";
    });
    document.addEventListener('click', function(event) {
        menuList.style.display = "none";
    });
    current.appendChild(textnode);
    box.appendChild(current);
    menuList = document.createElement("ul");
    var currentItem = document.createElement("li");
    textnode = document.createTextNode(languageNames[currentLang]);
    currentItem.appendChild(textnode);
    currentItem.addEventListener('click', function(event) {
        setLanguage(null);
    });
    menuList.appendChild(currentItem);
    for(var i = 0; i < langs.length; i++) {
        var item = document.createElement("li");
        textnode = document.createTextNode(languageNames[currentLang] + " - " + languageNames[langs[i]]);
        item.appendChild(textnode);
        item.myLang = langs[i];
        item.addEventListener('click', function(event) {
            setLanguage(event.target.myLang);
        });
        menuList.appendChild(item);
    }
    box.appendChild(menuList);
    box.setAttribute('id', 'lang-list');
    box.classList.add("menu");
    document.body.insertBefore(box, document.body.firstChild)
}

function setLanguage(otherLang) {
    if(status == null && otherLang == null) {
        return; /* nothing to do */
    } else if(otherLang == null) {
        status = otherLang;
        for(var i = 0; i < originalDom.length; i++) {
           document.body.appendChild(originalDom[i]);
        }
        document.body.removeChild(langTable);
        langTable = null;
        var textnode = document.createTextNode(languageNames[currentLang]);
        current.removeChild(current.firstChild);
        current.appendChild(textnode);
    } else {
        status = otherLang;
        var textnode = document.createTextNode(languageNames[currentLang] + " - " + languageNames[otherLang]);
        current.removeChild(current.firstChild);
        current.appendChild(textnode);
        var newLang = window.location.href.replace("/" + currentLang + "/", "/" + otherLang + "/");
        var iframe = document.createElement("iframe");
        iframe.setAttribute('src', newLang);
        iframe.addEventListener('load', function(event) {
            var iframeDocument = event.target.contentDocument;
            var newNodes = [];
            for(var i = 0; i < iframeDocument.body.childNodes.length; i++) {
                var node = iframeDocument.body.childNodes[i];
                if((node.nodeValue == null || node.nodeValue.trim().length != 0) && node.nodeType != Node.COMMENT_NODE && node.getAttribute && node.getAttribute('id') != 'lang-list') {
                    newNodes.push(node);
                }
            }
            if(langTable) {
                document.body.removeChild(langTable);
            }
            langTable = document.createElement("table");
            langTable.setAttribute('id', 'lang-table');
            var length = Math.max(originalDom.length, newNodes.length);
            for(var i = 0; i < length; i++) {
                var row = document.createElement("tr");
                var cellOne = document.createElement("td");
                if(originalDom[i]) {
                    cellOne.appendChild(originalDom[i]);
                }
                row.appendChild(cellOne);
                var cellTwo = document.createElement("td");
                if(newNodes[i]) {
                    cellTwo.appendChild(newNodes[i]);
                }
                row.appendChild(cellTwo);
                langTable.appendChild(row);
            }
            document.body.appendChild(langTable);
            iframe.parentNode.removeChild(iframe);
        });
        box.appendChild(iframe);
    }
}