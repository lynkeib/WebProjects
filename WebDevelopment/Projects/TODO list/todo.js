$("#textinput").keypress(function(event){
    if(event.keyCode == 13){
        // console.log(event)
        $("ul").append("<li><span><i class='far fa-trash-alt'></i></span>" + $("#textinput").val() + "</li>");
        $("#textinput").val("");
    }   
})

$(".fa-plus").on("click", function(){
    $("input").slideToggle();
})

$("ul").on("click", "li", function(){
    $(this).toggleClass("corssthetext");
})

$("ul").on("click", "span", function(event){
    $(this).parent().fadeOut(200, function(){
        $(this).remove();
    });
    event.stopPropagation();
})