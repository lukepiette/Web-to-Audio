function openUserAdd(event){
    // document.getElementById("add-user-click").style.transform = "translate3d(0px, 0px, 0px)";
    console.log(11);
    document.getElementById("add-user-click").style.visibility = "visible";
}

function closeUserAdd(event){
    // document.getElementById("add-user-click").style.transform = "translate3d(800px, 0px, 0px)";
    document.getElementById("add-user-click").style.visibility = "hidden";
}

function submitUserAdd(event){
    // document.getElementById("add-user-click").style.transform = "translate3d(800px, 0px, 0px)";
    document.getElementById("add-user-click").style.visibility = "hidden";
}

function addTagClick(event){
    document.getElementById("add-user-click").style.visibility = "visible";
}

function guidGenerator() {
    var S4 = function() {
        return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    };
    return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
}

function sleep (time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

function myLoop (nummy,name) {           //  create a loop function
    setTimeout(function () { 
        document.getElementById(name).childNodes[0].childNodes[1].childNodes[0].childNodes[3].innerHTML = nummy;
        nummy--;                     //  increment the counter
        if (nummy > -1) {            //  if the counter < 10, call the loop function
            myLoop(nummy,name);             //  ..  again which will trigger another 
        }                        //  ..  setTimeout()
    }, 40)
}

function checkBoxChecked(num){    
    // Color change + move right
    var names = ['connection-1','connection-2','connection-3','connection-4','connection-5','connection-6'];

    var move_len = parseInt(document.getElementById(names[num]).childNodes[0].childNodes[3].style.right) + 90;
    document.getElementById(names[num]).childNodes[0].childNodes[3].style.transition = "1s";
    document.getElementById(names[num]).childNodes[0].childNodes[3].style.transform = "translateX("+move_len+"px)";
    document.getElementById(names[num]).childNodes[0].childNodes[3].style.webkitTransition = "background-color 1500ms linear;";
    document.getElementById(names[num]).childNodes[0].childNodes[3].style.msTransition = "background-color 1500ms linear;";
    document.getElementById(names[num]).childNodes[0].childNodes[3].style.backgroundColor = "#a3f48f";
    document.getElementById(names[num]).childNodes[0].childNodes[3].style.borderRadius = "15px 15px 15px 15px";

    // Count down
    var nummy = parseInt(document.getElementById(names[num]).childNodes[0].childNodes[1].childNodes[0].childNodes[3].innerHTML);
    myLoop(nummy,names[num]);

    document.getElementById('add-a-note').style.transform = "translateX(0px)";
    document.getElementById('add-a-note').style.visibility = "visible";
    document.getElementById('note-content').innerHTML = "";
}
 
function myLoop2 (nummy,name) {           //  create a loop function
    setTimeout(function () { 
       document.getElementById(name).innerHTML = nummy  ; //  call a 3s setTimeout when the loop is called
       nummy--;                     //  increment the counter
       if (nummy > -1) {            //  if the counter < 10, call the loop function
          myLoop2(nummy,name);             //  ..  again which will trigger another 
       }                        //  ..  setTimeout()
    }, 40)
 }

function checkBoxCheckedProfile(){    
    // Color change + move right\\
    var name = 'days-since-contact-bar';
    var move_len = parseInt(document.getElementById(name).style.width) - 42;
    document.getElementById(name).style.transition = "1s";
    document.getElementById(name).style.transform = "translateX(" + move_len + "px)";
    document.getElementById(name).style.webkitTransition = "background-color 1500ms linear;";
    document.getElementById(name).style.msTransition = "background-color 1500ms linear;";
    document.getElementById(name).style.backgroundColor = "#a3f48f";
    document.getElementById(name).style.borderRadius = "20px 20px 20px 20px";
    // Count down
    var nummy = document.getElementById('days-since-contact-num').innerHTML;
    myLoop2(nummy,'days-since-contact-num');
}

function checkBoxChecked(num){    
    // Color change + move right
    var names = ['connection-1','connection-2','connection-3','connection-4','connection-5','connection-6'];

    var move_len = parseInt(document.getElementById(names[num]).childNodes[0].childNodes[3].style.right) + 90;
    document.getElementById(names[num]).childNodes[0].childNodes[3].style.transition = "1s";
    document.getElementById(names[num]).childNodes[0].childNodes[3].style.transform = "translateX("+move_len+"px)";
    document.getElementById(names[num]).childNodes[0].childNodes[3].style.webkitTransition = "background-color 1500ms linear;";
    document.getElementById(names[num]).childNodes[0].childNodes[3].style.msTransition = "background-color 1500ms linear;";
    document.getElementById(names[num]).childNodes[0].childNodes[3].style.backgroundColor = "#a3f48f";
    document.getElementById(names[num]).childNodes[0].childNodes[3].style.borderRadius = "15px 15px 15px 15px";

    // Count down
    var nummy = parseInt(document.getElementById(names[num]).childNodes[0].childNodes[1].childNodes[0].childNodes[3].innerHTML);
    myLoop(nummy,names[num]);

    document.getElementById('add-a-note').style.transform = "translateX(0px)";
    document.getElementById('add-a-note').style.visibility = "visible";
    document.getElementById('note-content').innerHTML = "";
}

function closeAddNote(){
    document.getElementById('add-a-note').style.visibility = "hidden";
    document.getElementById('note-content').innerHTML = "";
}


function addNote(){
    document.getElementById('added-note').innerHTML = document.getElementById('note-content').innerHTML;
    // document.getElementById('add-a-note').style.position = "absolute";
    document.getElementById('add-a-note').style.transform = "translateX(600px)";
    document.getElementById('add-a-note').style.visibility = "hidden";

    // document.getElementById('add-a-note').style.visibility = "hidden";
    // document.getElementById('add-a-note').style.transform = "translateX(0px)";
}



function showByColorBar(num){
    for (i=0;i<100;i++){
        try{
            if (parseInt(document.getElementById("connection-"+i.toString()).childNodes[0].childNodes[3].style.right) < num+11 && parseInt(document.getElementById("connection-"+i.toString()).childNodes[1].childNodes[7].style.right) > num-11){
                document.getElementById("connection-"+i.toString()).style.display = "block";
            }
            else{
                document.getElementById("connection-"+i.toString()).style.display = "none";
            }
        }
        catch{
        }
    }
}

function showAll(){
    for (i=0;i<100;i++){
        try{
            document.getElementById("connection-"+i.toString()).style.display = "block";
        }
        catch{
        }
    }
}

function userNotes(){
    document.getElementById('tracker-user').style.display = "none";
    document.getElementById('user-notes').style.visibility = "visible";
}

function userTracker(){
    document.getElementById('tracker-user').style.display = "inline";
    document.getElementById('user-notes').style.visibility = "hidden";
}

console.log("js loaded");