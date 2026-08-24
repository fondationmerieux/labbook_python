{#
    Adds the analyses picked in the search field to the current record, then
    goes back to the calling page.
    Define add_analysis_back_url before including this file.
#}
function add_analysis()
{
    let id_user        = {{ session['user_id']|safe}} ;
    let user_role      = "{{ session['user_role']|safe }}"  ;
    let id_rec         = data_res[0].id_dos ;
    let param_list_ana = '{ "list_ana":[ ';
    let param_list_res = '{ "id_owner":' + id_user + ', "user_role":"' + user_role + '", "list_ref":[ ';
    let value_ana      = '' ;
    let value_res      = '' ;

    // Add analysis
    for( i in list_id_ana )
    {
        if (value_ana != '')
        {
            value_ana += ', ' ;
        }

        if (value_res != '')
        {
            value_res += ', ' ;
        }

        let param_ana = '{ "id_owner":' + id_user + ', ' +
            '"id_rec":' + id_rec  + ', ' +
            '"id_ana":' + list_id_ana[i] + ', ' +
            '"price":0, ' +
            '"paid": 5, ' +
            '"emer": 5, ' +
            '"outsourced":"N", ' +
            '"req": 5 }' ;

        let param_res = '{ "ref_analyse":' + list_id_ana[i] + '}' ;

        value_ana += param_ana ;
        value_res += param_res ;
    }

    param_list_ana += value_ana + ' ] }';
    param_list_res += value_res + ' ] }';

    $("#dial-wait").off('shown.bs.modal') ;
    $("#dial-wait").modal("show") ;

    set_audit_context("{{ _('Analyse complémentaire') }}");

    // Send analysis information
    $.ajax( 
        {
            type: "POST",
            url: "{{ session['server_ext'] }}/services/analysis/list/req",
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            data: param_list_ana,
            headers: with_audit_headers({ 'Authorization': 'Bearer {{ session.get("be_access_token","") }}' }),
            success: function(ret_ana)
            {
                set_audit_context("{{ _('Analyse complémentaire') }}");
                // create in DB list of results to enter and corresponding validation
                $.ajax(
                    {
                        type : 'POST',
                        url : "{{ session['server_ext'] }}/services/result/create/" + id_rec,
                        dataType: 'json',
                        contentType: "application/json; charset=utf-8",
                        data: param_list_res,
                        headers: with_audit_headers({ 'Authorization': 'Bearer {{ session.get("be_access_token","") }}' }),
                        success : function(response)
                        {
                            let param_stat = '{ "stat":182 }' ; 

                            set_audit_context("{{ _('Analyse complémentaire') }}");

                            // update record stat to 182 = Validé administrativement
                            $.ajax(
                                {
                                    type : 'POST',
                                    url : "{{ session['server_ext'] }}/services/record/stat/" + id_rec,
                                    dataType: 'json',
                                    contentType: "application/json; charset=utf-8",
                                    data: param_stat,
                                    headers: with_audit_headers({ 'Authorization': 'Bearer {{ session.get("be_access_token","") }}' }),
                                    success : function(response)
                                    {
                                        $("#dial-wait").modal("hide") ;

                                        window.location.href = add_analysis_back_url + id_rec ;
                                    },
                                    error: function(response)
                                    {
                                        $("#dial-wait").modal("hide") ;

                                        console.log("ERROR record stat") ;
                                        alert("{{ _("Une erreur est survenue lors du changement de statut du dossier") }}") ;
                                    }
                                } ) ;
                        },
                        error: function(response)
                        {
                            $("#dial-wait").modal("hide") ;

                            console.log("ERROR result create") ;
                            alert("{{ _("Une erreur est survenue lors de la création des résultats") }}") ;
                        }
                    } ) ;
            },
            error: function(ret_ana)
            {
                $("#dial-wait").modal("hide") ;

                console.log("ERROR analysis list req") ;
                alert("{{ _("Une erreur est survenue lors de l'enregistrement des analyses") }}") ;
            } 
        } ) ;
}
