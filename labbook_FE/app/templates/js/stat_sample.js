function status_samp( samp_id, samp_stat, type_prel )
{
let res = '' ;
let btn = '' ;

    if ( samp_stat == 9 )
    btn = '<button type="button" onclick="det_sample(' + samp_id + ');" class="btn btn-danger">{{ _("A saisir") }}</button>' ;
    else if ( samp_stat == 8 || samp_stat == 10 )
    btn = '<button type="button" onclick="det_sample(' + samp_id + ');" class="btn btn-warning">{{ _("Modifier") }}</button>' ;

    res = btn + '<br><span class="text-muted">(' + type_prel + ')</span>';

return res ;
}

function det_sample(samp_id)
{
window.location = "{{ session['server_ext'] }}/det-sample/" + samp_id ;
}

