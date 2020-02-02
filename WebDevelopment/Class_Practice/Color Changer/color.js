var body = document.querySelectorAll('body');
var button = document.querySelectorAll('button');

function changecolor() {
    body[0].classList.toggle('changecolor');
}

button[0].addEventListener("click", changecolor);