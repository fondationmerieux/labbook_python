function display_histo( i )
{
$("#tbody_histo").empty() ;

let tr_histo = '<tr class="row"><td class=" col-1 icon"><span class="icon status-n">N</span></td>' +
               '<td class="col-2"><span id="date_rec">' + data_res[i].date_dos + '</span></td>' +
               '<td class="col"><ul style="padding:10px;"><li>{{ _("Création du dossier") }} (' + 
               {% if session['record_period'] == 1070 %}data_res[i].num_dos_mois{% else %}data_res[i].num_dos_an{% endif %} + ').</li>' +
               '<li>{{ _("Analyse demandée") }} : ' + data_res[i].nom + '</li>' +
               '<li>{{ _("Date de prescription") }} : ' + data_res[i].date_prescr + '.</li></ul></td></tr>' ;

    $.ajax( 
    {
        type: "GET",
        url: "/services/result/history/" + data_res[i].id_res,
        success: function(data_histo)
        {
            for( i in data_histo )
            {
            ident = '' ;
            extra = '' ;

                if ( data_histo[i].user != null )
                {
                    if ( data_histo[i].user.firstname  != "" )
                    ident += data_histo[i].user.firstname + ' ' ;

                    if ( data_histo[i].user.lastname  != "" )
                    ident += data_histo[i].user.lastname ;

                    if ( ident == "" )
                    ident += data_histo[i].user.username ;
                }

                if ( data_histo[i].motif_annulation != "" )
                extra += '<li><span>{{ _("ANNULE") }} ' + data_histo[i].dico_cancel.label +'</span></li>' ;

                if ( data_histo[i].commentaire != "" )
                extra += '<li><span>{{ _("Commentaire") }} : ' + data_histo[i].commentaire +'</span></li>'

            tr_histo += '<tr class="row"><td class="col-1 icon" id="stat_res">' + status_res( data_histo[i].type_validation ) + '</td>' +
                        '<td class="col-2"><span>' + data_histo[i].date_validation +'</span></td>' +
                        '<td class="col"><ul style="padding:10px;"><li><span>' + ident + '</span></li>' +
                        '<li><span>{{ _("Validation") }} ' + data_histo[i].dico_valid.label +'</span></li>' + extra + '</ul></td></tr>' ;
            }

            $("#tbody_histo").append(tr_histo) ;

            setTimeout(function()
            {
                $( "#dial-history" ).modal( "show" ) ;
            }, 600) ;
        },
        error: function(data_ana)
        {
            console.log("ERROR GET result history");
            alert("{{ _("Erreur lors la récupération des informations d'historiques de ce résultat") }}") ;
        }
    } ) ;
}
