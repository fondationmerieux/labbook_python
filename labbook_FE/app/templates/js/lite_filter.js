{#
    Shows the Lite user selector only when the Lite filter is set to "Y".
    Goes with lite-filter.html; call it from the page $(document).ready().
#}
    let lite_filter = $("#lite_filter").val() || "A" ;

    if (lite_filter === "Y")
    {
        $("#lite_user_container").show() ;
    }
    else
    {
        $("#lite_user_container").hide() ;
    }

    $("#lite_filter").on("change", function() {
        if ($(this).val() === "Y")
        {
            $("#lite_user_container").show() ;
        }
        else
        {
            $("#lite_user_container").hide() ;
            $("#lite_user_id").val("") ;
        }
    }) ;
