$("#textinput").keypress(function(event){
    if(event.keyCode == 13){
        // console.log(event)
        $("ul").append("<li>" + $("#textinput").val() + "</li>");
        $("#textinput").val("");
    }   
})