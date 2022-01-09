$(document).ready(function () {

    $("#launchBot").submit((e)=>{
        e.preventDefault();
        var data = {
            "query": $("#query").val(), 
            "headless": $("#headless").is(":checked"),
            "proxy": $("#proxy").val()
        }

        console.log(data);

        $.ajax({
            type: "post",
            headers: {"X-CSRFToken": document.getElementsByName('csrfmiddlewaretoken')[0].value},
            url: "/execution",
            data: data,
            success: function (response) {
                console.log(response);
                $("body").append($(`<div class='alert alert-success'>${JSON.stringify(response)}`))
            }
        });
    })

});