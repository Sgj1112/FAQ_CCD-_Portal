$(function() {

    $('#search').keyup(function() {

        $.ajax({
            type: "POST",
            url: "/tutorial/search/",
            // url: "{% url 'search_ques' %}",
            data: {
                'search_text' : $('#search').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });
});

function searchSuccess(data, textStatus, jqXHR)
{   
    // let lis = document.getElementById("mainlist");
    // console.log(sres.childNodes.length    )
        // lis.style.display = "none";

    $('#search-results').html(data)
}