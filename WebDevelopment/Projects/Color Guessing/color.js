var colorNum = 6;
var colors = colorGen(colorNum);

function colorGen(colorNum){
    var colors = [];
    for(var i = 0; i < colorNum; i++){
        colors.push(colorRandom())
    }
    return colors;
}

function colorRandom(){
    var R = String(Math.floor(Math.random() * 256));
    var G = String(Math.floor(Math.random() * 256));
    var B = String(Math.floor(Math.random() * 256));
    return "rgb(" + R + ", " + G + ", " + B + ")";
}

var squares = document.querySelectorAll(".square");
var pickedColor = colors[Math.floor(Math.random() * colors.length)];
var colordisplay = document.getElementById("colordisplay");
colordisplay.textContent = pickedColor;
var message = document.getElementById("message");



for(var i = 0; i < squares.length; i++){
    squares[i].style.backgroundColor = colors[i];
    squares[i].addEventListener("click", function(){
        if(this.style.backgroundColor === pickedColor){
            success()
            message.textContent = "Correct";;
        }else{
            this.style.backgroundColor = "#232323";
            message.textContent = "Try again";
        };
    });
}

function success(){
    for(var i = 0; i < squares.length; i++){
        squares[i].style.backgroundColor = pickedColor;
    };
};
