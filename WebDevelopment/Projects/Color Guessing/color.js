var colors = [
    "rgb(255, 255, 0)",
    "rgb(255, 0, 255)",
    "rgb(0, 255, 255)",
    "rgb(143, 255, 0)",
    "rgb(0, 43, 23)",
    "rgb(255, 2, 0)"
];

var squares = document.querySelectorAll(".square");
var pickedColor = colors[3];
var colordisplay = document.getElementById("colordisplay");
colordisplay.textContent = pickedColor;


for(var i = 0; i < squares.length; i++){
    squares[i].style.backgroundColor = colors[i];
    squares[i].addEventListener("click", function(){
        if(this.style.backgroundColor === pickedColor){
            success();
        }else{
            this.style.backgroundColor = "#232323";
        };
    });
}

function success(){
    for(var i = 0; i < squares.length; i++){
        squares[i].style.backgroundColor = pickedColor;
    };
};
