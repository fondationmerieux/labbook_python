/* javascript functions for labbook project */

// Return formatted record number
function fmt_num_rec( num_rec, fmt, period )
{
let ret = num_rec ;

    if ( fmt == 1072 ) // short format
    {
        if ( period == 1070 ) // month period
        ret = Number( (num_rec).substr(6,4) ) ; // convert number to take off front zero
        else
        ret = Number( (num_rec).substr(4,6) ) ;
    }

return ret ; 
}

// Return period for record number
function per_num_rec( num_rec, fmt, period )
{
let ret = "" ;

    if ( period == 1070 && fmt == 1072 ) // month period and short format
    ret = (num_rec).substr(4,2) + "/" + (num_rec).substr(0,4) ;

return ret ;
}
