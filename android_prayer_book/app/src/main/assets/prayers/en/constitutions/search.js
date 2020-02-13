var index_data = {};
var norm_index = {};
var art_index = {};

var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};

function loadGoTo() {
    getJSON('index.json',
        function(err, data) {
          if (err !== null) {
            // fail
          } else {
            index_data = data;
          }
        });
}



function goToArt(event) {
    event.preventDefault();
    var artNum = document.getElementById('art-number').value;
    for (const art of index_data['articles']){
        if(art['id'] == artNum) {
            document.location = art['doc'] + '#art' + artNum;
        }
    }
}

function goToNorm(event) {
    event.preventDefault();
    var normNum = document.getElementById('norm-number').value;
    for (const norm of index_data['norms']){
        if(norm['id'] == normNum) {
            document.location = norm['doc'] + '#norm' + normNum;
        }
    }
}

function loadSearch() {
    getJSON('index.json',
        function(err, data) {
            if (err !== null) {
                // fail
            } else {
                index_data = data;
            }

            art_index = elasticlunr(function () {
                this.addField('body');
                this.setRef('id');
            });

            for (const art of index_data['articles']){
                art_index.addDoc(art);
            }

           norm_index = elasticlunr(function () {
               this.addField('body');
               this.setRef('id');
           });

           for (const art of index_data['norms']){
               norm_index.addDoc(art);
           }
   });
}

function getDataRow(data, row) {
   for (const d of data){
       if(d['id'] == row) {
            return d;
       }
   }
}

function search(event) {
    event.preventDefault();
    var index = art_index;
    var data = index_data['articles'];
    var title = "Article ";
    var link = "art";
    if(document.getElementById('directory-radio').checked) {
        var index = norm_index;
        var data = index_data['norms'];
        var title = "Norm "
        var link = 'norm';
    }
    var results = document.getElementById('results');
    while (results.firstChild) {
        results.removeChild(results.firstChild);
    }
    var term = document.getElementById('searchbox').value
    var values = index.search(term);

    tokens = elasticlunr.tokenizer(term);
    for(var i = 0; i < tokens.length; i++) {
        tokens[i] = elasticlunr.stemmer(tokens[i]);
    }
    for(const value of values) {
        var row_data = getDataRow(data, value['ref'])
        var row = document.createElement('div');
        var h2 = document.createElement('h2');
        var a = document.createElement('a');
        var href = row_data['doc'] + '#' + link + value['ref'];
        a.setAttribute('href', href);
        a.textContent = title + value['ref'];
        h2.appendChild(a);
        row.appendChild(h2);

        var row_text = document.createElement('div');
        var result_body = row_data['body']
        result_body = result_body.replace(/\w+/g, (matched, index, original) => {
            var stem = elasticlunr.stemmer(matched.toLowerCase());
            if(tokens.includes(stem)) {
                return "<strong>" + matched + "</strong>";
            } else {
                return matched;
            }
        });
        row_text.innerHTML = result_body;
        row.appendChild(row_text);
        results.appendChild(row);
    }
}