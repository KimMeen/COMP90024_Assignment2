
var url = "http://172.26.37.207:8080/"
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
    data_name = document.getElementById("selectData").value
    document.getElementById("selectData").value = data_name
    var xmlHttp = new XMLHttpRequest();
    var request = url+ "regionCount/"+data_name
    console.log(request)
    var value = localStorage.getItem("pick_")
    if(value) {request= url + "regionCount/"+value}
    xmlHttp.open("GET", request, false);
    xmlHttp.send();
    var obj = JSON.parse(xmlHttp.responseText);
    console.log(obj)
    return obj;
};


function reloadChart(){
    console.log("hihihi")
    pick_ = document.getElementById("selectCity").value;
    localStorage.pick_ = pick_
    pick_ = localStorage.getItem("pick_");
    window.location.reload();
};

function getLastSelectedCity(){
     var value = localStorage.getItem("pick_")
     if(value){document.getElementById("selectCity").value = value;}
     return value
}

function getCityTweetsData(dataType){
    data_name = document.getElementById("selectCity").value
    console.log("hi there" +data_name)
    
    var xmlHttp = new XMLHttpRequest();
    var request = url+"tweet_data/" + data_name +"/"+ dataType
    var value = localStorage.getItem("pick_")
    if(value) {request= url+"tweet_data/"+value+"/"+dataType}

    console.log(request)
    xmlHttp.open("GET", request, false);
    xmlHttp.send();
    var obj = JSON.parse(xmlHttp.responseText);
    console.log(obj)
    return obj;
};


function getCityData(){
    data_name = document.getElementById("selectCity").value
    var xmlHttp = new XMLHttpRequest();
    var request = url+"aurin/Melbourne/lung_cancer.json"
    console.log(request)
    xmlHttp.open("GET", request, false);
    xmlHttp.send();
    var obj = JSON.parse(xmlHttp.responseText);
    console.log(obj)
    return obj;
};

