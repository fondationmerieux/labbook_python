function pat_ident( lastname, maidenname, firstname )
{
let res = "" ;

    if (lastname != "" || lastname != null)
    res += lastname + " " ;

    if (maidenname != "" || maidenname != null)
    res += maidenname + " " ;

    if (firstname != "" || firstname != null)
    res += firstname + " " ;

    if (res == "")
    res += "{{ _("Anonyme") }}" ;

return res ;
}
