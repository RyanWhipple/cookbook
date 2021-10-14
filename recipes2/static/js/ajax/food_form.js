$(document).ready(function(){
    $('#picture').change(function(){
        var data = new FormData($('#food_form')[0])
        $.ajax({
            method:'POST',
            url:'/ajax/image/update/recipe_pics',
            data:data,
            contentType:false,
            cache:false,
            processData:false,
            success: function(results) {
            $('#image').prop('src',`/static/recipe_pics/${results}`);
            },
        })
    });
    $("#prep_time,#cook_time").keyup(function(){
        if(isNaN($(this).val())){
            $(this).addClass('is-invalid');
        }else{
            $(this).removeClass('is-invalid');
        }
    })
});