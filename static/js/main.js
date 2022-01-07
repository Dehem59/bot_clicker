$(document).ready(function () {

    $("#launchBot").submit((e)=>{
        e.preventDefault();
        $.ajax({
            type: "post",
            headers: {"X-CSRFToken": document.getElementsByName('csrfmiddlewaretoken')[0].value},
            url: "/gui/execution",
            data: {
                "test": "data test"
            },
            success: function (response) {
                console.log(response);
                $("body").append($(`<div class='alert alert-success'>${JSON.stringify(response)}`))
            }
        });
    })

});