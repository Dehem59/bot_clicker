$(document).ready(function () {

    $("#launchBot").submit((e)=>{
        e.preventDefault();

        $("body nav").after($(`<div class="container"><div class="row">
        <img id='loader' src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Loader.gif/480px-Loader.gif'
        class='img-fluid mx-auto text-center col-md-2'/></div></div>`));
        var data = {
            "query": $("#query").val(), 
            "proxy": $("#proxy").val(),
            "domaine" : $("#domaine").val(),
            "user_agent": $("#user_agent").val(),
            "ads_mode": $("#ads").is(":checked")
        }

        console.log(data);

        $.ajax({
            type: "post",
            headers: {"X-CSRFToken": document.getElementsByName('csrfmiddlewaretoken')[0].value},
            url: "/execution/",
            data: data,
            success: function (response) {
                console.log(response);
                $("#loader").css("display", "none");
                $("body").append($(`<div class='alert alert-success'>${JSON.stringify(response)}</div>`))
            },
            error: (response) => {
                console.log(response);
                $("#loader").css("display", "none");
                $("body").append($(`<div class='alert alert-danger'>${JSON.stringify(response.responseJSON)}</div>`))
            }
        });
    })

});
