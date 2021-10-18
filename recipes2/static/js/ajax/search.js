$(document).ready(function(){
    $("#q").keyup(function(){
        data = `q=${$("#q").val()}`
        $.ajax({
            method:"GET",
            url:'/ajax/search',
            data:data
        }).done(function(results){
            $("#results_div").html(results)
        })
    })
});