$(document).ready(function(){
    $('#picture').change(function(){
        var data = new FormData($('#food_form')[0])
        // console.log(data)
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
});