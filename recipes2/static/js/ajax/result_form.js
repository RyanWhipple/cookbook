var validators = {'snippet':false,'picture':false}
$(document).ready(function(){
    checkValid();
    $('#picture').change(function(){
        var data = new FormData($('#result_form')[0])
        // console.log(data)
        $.ajax({
            method:'POST',
            url:'/ajax/image/update/result_pics',
            data:data,
            contentType:false,
            cache:false,
            processData:false,
            success: function(results) {
            $('#image').prop('src',`/static/result_pics/${results}`);
            validators['picture']=true;
            checkValid();
            },
        })
    });
    $('#snippet').keyup(function(){
        if($('#snippet').val().length < 5){
            $('#snippet_message').html("Notes must be at least 5 characters")
            $('#snippet').addClass('is-invalid')
            validators['snippet']=false;
            checkValid();
        }else{
            $('#snippet_message').html("")
            $('#snippet').removeClass('is-invalid')
            validators['snippet']=true;
            checkValid();
        }
    });
});
function checkValid(){
    if (Object.values(validators).every(validator => validator==true)){
        $('#submit').prop('disabled',false);
    }else{
        $('#submit').prop('disabled',true);
    }
}