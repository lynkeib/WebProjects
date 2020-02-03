var colorNum = 6;
var colors = colorGen(colorNum);
var squares = document.querySelectorAll(".square");
var pickedColor = colors[Math.floor(Math.random() * colors.length)];
var colordisplay = document.getElementById("colordisplay");
colordisplay.textContent = pickedColor;
var message = document.getElementById("message");
var resetButton = document.querySelector("#resetButton");
var mode = document.querySelectorAll(".mode");


function colorGen(colorNum){
    var colors = [];
    for(var i = 0; i < colorNum; i++){
        colors.push(colorRandom())
    }
    return colors;
};

function colorRandom(){
    var R = String(Math.floor(Math.random() * 256));
    var G = String(Math.floor(Math.random() * 256));
    var B = String(Math.floor(Math.random() * 256));
    return "rgb(" + R + ", " + G + ", " + B + ")";
};

function success(){
    for(var i = 0; i < squares.length; i++){
        squares[i].style.backgroundColor = pickedColor;
    };
    console.log(document.querySelector("h1"));
    document.querySelector("h1").style.backgroundColor = pickedColor;
    resetButton.textContent = "Play Again?"
};

function reset(){
    resetButton.textContent = "New Color";
    colors = colorGen(colorNum);
    pickedColor = colors[Math.floor(Math.random() * colors.length)];
    colordisplay.textContent = pickedColor;
    for(var i=0; i < squares.length; i++){
        if(colors[i]){
            squares[i].style.display = 'block';
            squares[i].style.backgroundColor = colors[i];
        }else{
            squares[i].style.display = 'none';
        }
    };
};

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
};

resetButton.addEventListener("click", function(){
    message.textContent = "";
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
});

for(var i=0; i < mode.length; i++){
    mode[i].addEventListener("click", function(){
        mode[0].classList.remove("selected");
        mode[1].classList.remove("selected");
        this.classList.add("selected");
        this.textContent=="Easy" ? colorNum = 3: colorNum = 6;
        reset();
    })
};