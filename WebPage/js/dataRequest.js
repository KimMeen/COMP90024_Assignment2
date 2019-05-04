function getMapData(){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", 'http://127.0.0.1:5000/db/tweets', false);
    xmlHttp.send();
    var obj = JSON.parse(xmlHttp.responseText);
    return obj;
};

