
function getLastSelectedValue(){
     var value = localStorage.getItem("pick_")
     if(value){document.getElementById("selectData").value = value;}
     return value
}

function getMapData(){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", 'http://172.26.37.207:5000/data', false);
    xmlHttp.send();
    var obj = JSON.parse(xmlHttp.responseText);
    return obj;
};

function reload(){
    pick_ = document.getElementById("selectData").value;
    localStorage.pick_ = pick_
    pick_ = localStorage.getItem("pick_");
    console.log(pick_)
    window.location.reload();
};

function getRegionView(){
    data_name = document.getElementById("selectData").value
    var xmlHttp = new XMLHttpRequest();
    var request = "http://172.26.37.207:5000/regionCount/"+data_name
    var value = localStorage.getItem("pick_")
    if(value) {request= "http://172.26.37.207:5000/regionCount/"+value}
    console.log(request)
    xmlHttp.open("GET", request, false);
    xmlHttp.send();
    var obj = JSON.parse(xmlHttp.responseText);
    return obj;
};

