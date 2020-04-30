/* javascript functions for labbook project */

// Return formatted record number
function fmt_num_rec( num_rec, fmt, period )
{
let ret = num_rec ;

    if ( fmt == 1072 ) // short format
    {
        if ( period == 1070 ) // month period
        ret = Number( (num_rec.toString()).substr(6,4) ) ; // convert number to take off front zero
        else
        ret = Number( (num_rec.toString()).substr(4,6) ) ;
    }

return ret ; 
}

// Return period for record number
function per_num_rec( num_rec, fmt, period )
{
let ret = "" ;

    if ( period == 1070 && fmt == 1072 ) // month period and short format
    ret = (num_rec.toString()).substr(4,2) + "/" + (num_rec.toString()).substr(0,4) ;

return ret ;
}

function stat( id_stat )
{
let res = '' ;

    if ( id_stat == 182 )
    res = '<span class="icon status-a">A</span>' ;
    else if ( id_stat == 253 )
    res = '<span class="icon status-a">I</span>' ;
    else if ( id_stat == 254 )
    res = '<span class="icon status-t">T</span>' ;
    else if ( id_stat == 255 )
    res = '<span class="icon status-t">I</span>' ;
    else if ( id_stat == 256 )
    res = '<span class="icon status-b">B</span>' ;

return res ;
}

function emer( flag_emer )
{
let res = '' ;

    if ( flag_emer == "O" || flag_emer == 4 )
    res = '<span class="icon urgent">&nbsp;</span>' ;

return res ;
}
