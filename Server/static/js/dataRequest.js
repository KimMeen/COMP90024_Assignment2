var url = "http://127.0.0.1:8080/"

function getLastSelectedValue(){
     var value = localStorage.getItem("pick_")
     if(value){document.getElementById("selectData").value = value;}
     return value
}
function getMapData(){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url + "data", false);
    xmlHttp.send();
    var obj = JSON.parse(xmlHttp.responseText);
    return obj;
};

function reload(){
    pick_ = document.getElementById("selectData").value;
    localStorage.pick_ = pick_
    pick_ = localStorage.getItem("pick_");
    window.location.reload();
};

function getRegionView(){
    data_name = document.getElementById("selectData").value;
    document.getElementById("selectData").value = data_name;
    var xmlHttp = new XMLHttpRequest();
    var request = url+ "regionCount/"+data_name;
    var last_data_name = localStorage.getItem("pick_")
    var value = localStorage.getItem("pick_")
    if (value) {request = url+ "regionCount/"+last_data_name;}
    xmlHttp.open("GET", request, false);
    xmlHttp.send();
    var obj = JSON.parse(xmlHttp.responseText);
    console.log(obj)
    return obj;
};


function getCityTweetsData(dataType){
    data_name = document.getElementById("selectCity").value
    var xmlHttp = new XMLHttpRequest();
    var request = url+"tweet_data/" + data_name +"/"+ dataType
    console.log(request)
    xmlHttp.open("GET", request, false);
    xmlHttp.send();
    var obj = JSON.parse(xmlHttp.responseText);
    console.log(obj)
    return obj;
};


function getPieChartData(){
    var xmlHttp = new XMLHttpRequest();
    var request = url+"pieChart"
    console.log(request)
    xmlHttp.open("GET", request, false);
    xmlHttp.send();
    var obj = JSON.parse(xmlHttp.responseText);
    return obj;
}



function getCitySentData(){
    city = document.getElementById("selectCity").value
    var xmlHttp = new XMLHttpRequest();
    var request = url+"citySentData/"+city
    console.log(request)
    xmlHttp.open("GET", request, false);
    xmlHttp.send();
    var obj = JSON.parse(xmlHttp.responseText);
    return obj;
}

