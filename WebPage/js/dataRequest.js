function getMapData(){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", 'http://127.0.0.1:5000/test_data', false);
    xmlHttp.send();
    var obj = JSON.parse(xmlHttp.responseText);
    return obj;
};
