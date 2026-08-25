{#
    Asks for confirmation, then deletes an attached document and reloads the page.
#}
function delete_file( type_ref, id_file )
{
    if ( window.confirm("{{ _("Le fichier sera définitivement supprimé") }}") )
    {
        // popup wait
        $("#dial-wait").off('shown.bs.modal') ;
        $("#dial-wait").modal("show") ;

        $.ajax(
        {
            type: "DELETE",
            url: "{{ session['server_ext'] }}/services/file/document/" + type_ref + "/" + id_file,
            headers: { 'Authorization': 'Bearer {{ session.get("be_access_token","") }}' },
            success: function(ret)
            {
            $("#dial-wait").modal("hide") ;
            location.reload() ;
            },
            error: function(ret)
            {
            console.log("ERROR DELETE document file") ;
            $("#dial-wait").modal("hide") ;
            alert("{{ _("Erreur lors de la suppression d'un fichier") }}") ;
            }
        } ) ;
    }
    else
    return false ;
}
