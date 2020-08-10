$(function() {

    $.ajax({
            type: "POST",
            url: "/tutorial/sort/",
            data: {
                'search_text' : "latest",
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
     $("#sort").change(function () {
        var Selected = $('#sort').find("option:selected");
        var valueSelected  = Selected.val();

        $.ajax({
            type: "POST",
            url: "/tutorial/sort/",
            data: {
                'search_text' : valueSelected,
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

    $('#sort-result').html(data)
}