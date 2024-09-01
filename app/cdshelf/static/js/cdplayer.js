document.getElementById("pause").onclick = function(){
    fetch("/cdshelf/pause").catch(err => console.log(err));
};
document.getElementById("play").onclick = function(){
    fetch("/cdshelf/play").catch(err => console.log(err));
};
document.getElementById("eject").onclick = function(){
    fetch("/cdshelf/eject").catch(err => console.log(err));
};
document.getElementById("next").onclick = function(){
    fetch("/cdshelf/next").catch(err => console.log(err));
};
document.getElementById("previous").onclick = function(){
    fetch("/cdshelf/previous").catch(err => console.log(err));
};

var insertElems = document.querySelectorAll('.insert');
for (var i=insertElems.length; i--;) {
    insertElems[i].addEventListener('click', insert, false);
}
function insert() {
    console.log("Click!");
    fetch("/cdshelf/play?"+ new URLSearchParams({
        cd_id: this.getAttribute("cd"),
        track: this.getAttribute("track"),
    }).toString()).catch(err => console.log(err));
};
