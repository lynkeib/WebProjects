var color = [
    "rgb(255, 255, 0)",
    "rgb(255, 0, 255)",
    "rgb(0, 255, 255)",
    "rgb(143, 255, 0)",
    "rgb(0, 43, 23)",
    "rgb(255, 2, 0)"
];

var squares = document.querySelectorAll(".square");
var pickedColor = colors[3];



for(var i = 0; i < squares.length; i++){
    squares[i].style.backgroundColor = color[i];
}
