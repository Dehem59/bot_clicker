$(document).ready(function () {

    $("#launchBot").submit((e)=>{
        e.preventDefault();
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
            url: "/execution-ads/",
            data: data,
            success: function (response) {
                console.log(response);
                $("body").append($(`<div class='alert alert-success'>${JSON.stringify(response)}</div>`))
            },
            error: (response) => {
                console.log(response);
                $("body").append($(`<div class='alert alert-danger'>${JSON.stringify(response.responseJSON)}</div>`))
            }
        });
    })

});
