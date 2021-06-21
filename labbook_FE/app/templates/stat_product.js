function status_samp( samp_id, samp_stat )
{
let res = '' ;

    if ( samp_stat == 9 )
    res = '<button type="button" onclick="det_sample(' + samp_id + ');" class="btn btn-danger">{{ _("A saisir") }}</span>' ;
    else if ( samp_stat == 8 || samp_stat == 10 )
    res = '<button type="button" onclick="det_sample(' + samp_id + ');" class="btn btn-warning">{{ _("Modifier") }}</span>' ;

return res ;
}

function det_sample(samp_id)
{
window.location = "{{ session['server_ext'] }}/{{ session['redirect_name'] }}/det-sample/" + samp_id ;
}

