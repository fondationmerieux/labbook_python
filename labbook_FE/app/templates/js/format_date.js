/**
 * Formats an ISO date (YYYY-MM-DD, with or without a time) the way the language of the
 * session expects. The value is returned unchanged when it is empty or not a date, so a
 * display never breaks on it.
 */
function format_date( value )
{
    if (!value)
    return "" ;

let base  = value.split("T")[0].split(" ")[0] ;
let parts = base.split("-") ;

    if (parts.length != 3)
    return value ;

{% if session['date_format'] == '%m/%d/%Y' %}
    return parts[1] + "/" + parts[2] + "/" + parts[0] ;
{% else %}
    return parts[2] + "/" + parts[1] + "/" + parts[0] ;
{% endif %}
}
