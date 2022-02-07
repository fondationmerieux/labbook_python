function status_rec_with_det( id_stat, id_rec, rec_num )
{
let res = '' ;
let popup_det = 'onclick="det_stat_rec(' + id_rec + ', \'' + rec_num + '\');"' ;

    if ( id_stat == 182 )
    res = '<span class="icon stat-A cursor-act" ' + popup_det + '>A</span>' ;
    else if ( id_stat == 253 )
    res = '<span class="icon stat-A cursor-act" ' + popup_det + '>I</span>' ;
    else if ( id_stat == 254 )
    res = '<span class="icon stat-T cursor-act" ' + popup_det + '>T</span>' ;
    else if ( id_stat == 255 )
    res = '<span class="icon stat-T cursor-act" ' + popup_det + '>I</span>' ;
    else if ( id_stat == 256 )
    res = '<span class="icon stat-B cursor-act" ' + popup_det + '>B</span>' ;

return res ;
}

function det_stat_rec(id_rec, rec_num)
{
    $("#tbody_det_rec").empty() ;
    $("#det_rec_num").text( rec_num ) ;

let tr_det_rec = '' ;

    $.ajax( 
    {
        type: "GET",
        url: "{{ session['server_ext'] }}/services/record/list/analysis/" + id_rec,
        success: function(data_rec)
        {
            for( i in data_rec )
            {
            tr_det_rec += '<tr><td class="col-1 icon">' + status_res( data_rec[i].last_vld ) + '</td>' +
                          '<td>' + data_rec[i].name + '</td></tr>' ;
            }

            $("#tbody_det_rec").append(tr_det_rec) ;

            setTimeout(function()
            {
                $( "#dial-det-rec" ).modal( "show" ) ;
            }, 500) ;
        },
        error: function(ret)
        {
            if (ret.status != 404)
            {
            console.log("ERROR GET record list analysis ret=" + ret.status);
            alert("{{ _("Une erreur est survenue lors de la récupération des données") }}") ;
            }
        }
    } ) ;
}
