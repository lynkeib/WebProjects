var input = document.querySelectorAll("input")[0];
var playerone_button = document.querySelectorAll("#playerone-button")[0];
var playertwo_button = document.querySelectorAll("#playertwo-button")[0];
var playerone_score = 0;
var playertwo_score = 0;
var playingto = document.querySelectorAll("#playingto")[0];
var reset = document.querySelectorAll("#reset")[0];

input.addEventListener("input", function(){
    playingto.textContent = Number(this.value);
});

function winner(){
    if(playerone_score + playertwo_score >= playingto.textContent){
        if(playerone_score > playertwo_score){
            document.querySelectorAll("#playerone")[0].classList.add("winer");
        }
        else if(playerone_score < playertwo_score) {
            document.querySelectorAll("#playertwo")[0].classList.add("winer")
        };
    };
};

playerone_button.addEventListener("click", function(){
    if(playerone_score + playertwo_score >= playingto.textContent){
        return;
    }
    playerone_score++;
    document.querySelectorAll("#playerone")[0].textContent = playerone_score;
    // console.log(playerone_score + playertwo_score, playingto);
    winner();
});

playertwo_button.addEventListener("click", function(){
    if(playerone_score + playertwo_score >= playingto.textContent){
        return;
    }
    playertwo_score++;
    document.querySelectorAll("#playertwo")[0].textContent = playertwo_score;
    // console.log(playerone_score + playertwo_score, playingto);
    winner();
});

reset.addEventListener("click", function(){
    if(playerone_score > playertwo_score){
        document.querySelectorAll("#playerone")[0].classList.remove("winer");
    }
    else if(playerone_score < playertwo_score){
        document.querySelectorAll("#playertwo")[0].classList.remove("winer");
    };
    playerone_score = 0;
    playertwo_score = 0;
    document.querySelectorAll("#playerone")[0].textContent = 0;
    document.querySelectorAll("#playertwo")[0].textContent = 0;
});