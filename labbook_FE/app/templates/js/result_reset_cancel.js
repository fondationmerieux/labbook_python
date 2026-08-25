{#
    Result reset and cancel handling shared by the technical and biological validation pages.
    Requires the globals id_rec_tmp and id_res_tmp, and the #dial-cancel modal.
    Set result_return_page before including to the route the page reloads on success.
#}
function reset_res( id_rec, id_res )
{
    if ( window.confirm("{{ _("Etes-vous sur de vouloir effacer ce résultat ?") }}") )
    {
    let param_res = '{ "id_owner": {{ session["user_id"]}}, "id_res":' + id_res + '}' ;

    set_audit_context("{{ _('Résultat réinitialisé') }}");

        // result to reset
        $.ajax( 
        {
            type: "POST",
            url: "{{ session['server_ext'] }}/services/result/reset/" + id_rec,
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            data: param_res,
            headers: with_audit_headers({ 'Authorization': 'Bearer {{ session.get("be_access_token","") }}' }),
            success: function(data)
                {
                window.location.href = "{{ session['server_ext'] }}/{{ result_return_page }}/{{ ihm['mode'] }}/" + id_rec ;
                },
            error: function(data)
                {
                console.log("ERROR result reset") ;
                alert("{{ _("Une erreur est survenue lors de réinitialisation d'une valeur saisie") }}") ;
                }
        } ) ;
    }
}

function cancel_res( id_rec, id_res )
{
    if ( window.confirm("{{ _("Etes-vous sur de vouloir annuler ce résultat ?\\nCette action est irreversible.") }}") )
    {
    id_rec_tmp = id_rec ;
    id_res_tmp = id_res ;

        // popup reason and comment
        $( "#dial-cancel" ).modal( "show" ) ;
    }
    else
    {
    id_rec_tmp = 0 ;
    id_res_tmp = 0 ;
    }
}

function send_cancel()
{
let reason    = $("#cancel_reason").val() ;
let comment   = JSON.stringify( $.trim( $("#cancel_comm").val() ) ) ;
let param_res = '{ "id_owner": {{ session['user_id']}}, ' +
                  '"id_res":' + id_res_tmp + ', ' +
                  '"reason":' + reason + ',' +
                  '"comment":' + comment  + '}' ; // NO QUOTE DUE TO STRINGIFY PROCESS

    $('#dial-cancel').modal("hide") ;

    set_audit_context("{{ _('Résultat annulé') }}");

    // result to cancel
    $.ajax( 
    {
        type: "POST",
        url: "{{ session['server_ext'] }}/services/result/cancel/" + id_rec_tmp,
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        data: param_res,
        headers: with_audit_headers({ 'Authorization': 'Bearer {{ session.get("be_access_token","") }}' }),
        success: function(data)
            {
            window.location.href = "{{ session['server_ext'] }}/{{ result_return_page }}/{{ ihm['mode'] }}/" + id_rec_tmp ;
            },
        error: function(data)
            {
            console.log("ERROR result cancel") ;
            alert("{{ _("Une erreur est survenue lors de l'annulation d'une valeur saisie") }}") ;
            }
    } ) ;
}
