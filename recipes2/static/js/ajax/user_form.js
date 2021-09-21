var validators = {'username':false,'email':false,'password':false,'confirm_password':false}
$(document).ready(function(){
    $('#submit').prop('disabled',true);
    Object.keys(validators).forEach(validator => {
        $(`#${validator}`).keyup(function(){checkValid(validator)});
    });
});
function checkValid(id){
    var data = $("#regform").serialize()
    $.ajax({
            method:'POST',
            url:`/ajax/user/${id}`,
            data:data
    })
    .done(function(results){
        validators[id]=(results.length < 3);
        $(`#${id}_message`).html(results);
        if(Object.values(validators).every(validator => validator === true)){
            $('#submit').prop('disabled',false);
        }else{
            $('#submit').prop('disabled',true);
        }
    });
}