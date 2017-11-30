function  moveon () {
    var answer = confirm("准备好了吗？");
    if (answer) window.location = "http:\\baidu.com"
}
setTimeout(moveon,100)

function debug(msg) {
    var log = document.getElementById("debuglog");
    if (!log){
        log = document.createElement("div");
        log.id = "debuglog";
        log.innerHTML = "<h1>Debug Log</h1>";
        document.body.appendChild(log)
    }
    var pre = document.createElement("pre");
    var text = document.createTextNode(msg);
    pre.appendChild(text);
    log.appendChild(pre);
}

function hide(e , reflow) {
    if (reflow) {
        e.style.display = "none";
    }
    else {
        e.style.visibility = "hidden";
    }
}

function highlight(e) {
    if (!e.className){
        e.className = "hilite";
    }
    else {
        e.className += "hilite";
    }
}

window.onload = function () {
    var images = document.getElementsByTagName("image");
    for ( var i = 0; i<=images.length ; i++){
        var image = images[i];
        if (image.addEventListener){
            image.addEventListener("click",hide,false);
        }
        else {
            image.attachEvent("onclick",hide);
        }
    }
    function hide(event) {
        event.target.style.visibility = "hidden";
    }
}