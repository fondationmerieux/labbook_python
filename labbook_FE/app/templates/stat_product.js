function status_prod( prod_id, prod_stat )
{
let res = '' ;

    if ( prod_stat == 9 )
    res = '<button type="button" onclick="det_product(' + prod_id + ');" class="btn btn-danger">{{ _("A saisir") }}</span>' ;
    else if ( prod_stat == 8 || prod_stat == 10 )
    res = '<button type="button" onclick="det_product(' + prod_id + ');" class="btn btn-warning">{{ _("Modifier") }}</span>' ;

return res ;
}

function det_product(prod_id)
{
window.location = "{{ session['server_ext'] }}/{{ session['redirect_name'] }}/det-product/" + prod_id ;
}

