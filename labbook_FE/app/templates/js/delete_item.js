function delete_item(id_item, url_service)
{
var id_user = {{ session['user_id']|safe}} ;

    if ( window.confirm("{{ _("Merci de confirmer la suppression") }}") )
    {
    var param = '{ "id_user":' + id_user + '}' ;

        // popup wait
        $("#dial-wait").off('shown.bs.modal') ;
        $("#dial-wait").modal("show") ;

        $.ajax( 
        {
            type: "DELETE",
            url: "{{ session['server_ext'] }}/ajax/" + url_service + id_item,
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            data: param,
            success: function(ret)
            {
            $("#dial-wait").modal("hide") ;
            location.reload() ;
            },
            error: function(ret)
            {
            console.log("ERROR DELETE item") ;
            $("#dial-wait").modal("hide") ;
            alert("{{ _("Erreur lors de la suppression des données") }}") ;
            }
        } ) ;
    }
    else
    return false ; 
}
