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
    console.log(document.querySelector("h1"));
    document.querySelector("h1").style.backgroundColor = pickedColor;
    resetButton.textContent = "Play Again?"
};

var resetButton = document.querySelector("#resetButton");
resetButton.addEventListener("click", function(){
    colors = colorGen(colorNum);
    pickedColor = colors[Math.floor(Math.random() * colors.length)];
    colordisplay.textContent = pickedColor;
    for(var i = 0; i < squares.length; i++){
        if(colors[i]){
            squares[i].style.backgroundColor = colors[i];
            squares[i].style.display = 'block';
            squares[i].addEventListener("click", function(){
                if(this.style.backgroundColor === pickedColor){
                    success()
                    message.textContent = "Correct";;
                }else{
                    this.style.backgroundColor = "#232323";
                    message.textContent = "Try again";
                };
            });
        } else {
            squares[i].style.display = 'none';
        };
    }
    this.textContent = "New Color";
    document.querySelector("h1").style.backgroundColor = null;
})

var easy = document.querySelector("#easy");
var hard = document.querySelector("#hard");

easy.addEventListener("click", function(){
    document.querySelector('h1').style.backgroundColor = "steelblue";
    this.classList.add("selected");
    hard.classList.remove("selected");
    colorNum = 3;
    colors = colorGen(colorNum);
    pickedColor = colors[Math.floor(Math.random() * colors.length)];
    colordisplay.textContent = pickedColor;
    for(var i=0; i < squares.length; i++){
        if(colors[i]){
            squares[i].style.backgroundColor = colors[i];
        }else{
            squares[i].style.display = 'none';
        }
    }
})

hard.addEventListener("click", function(){
    document.querySelector('h1').style.backgroundColor = "steelblue";
    this.classList.add("selected");
    easy.classList.remove("selected");
    colorNum = 6;
    colors = colorGen(colorNum);
    pickedColor = colors[Math.floor(Math.random() * colors.length)];
    colordisplay.textContent = pickedColor;
    for(var i=0; i < squares.length; i++){
        squares[i].style.backgroundColor = colors[i];
        squares[i].style.display = 'block';
    }
})
