/* javascript functions for labbook project */
var disconnect_page = "/sigl/auth/index/disconnect" ;
var page_timeout    = 0 ;

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

function status_rec( id_stat )
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

function status_res( id_stat )
{
let res = '' ;

    if ( id_stat == 250 )
    res = '<span class="icon status-a">A</span>' ;
    else if ( id_stat == 251 )
    res = '<span class="icon status-t">T</span>' ;
    else if ( id_stat == 252 )
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

function init_timeOut( url_server, logout_time )
{
let disconnect_time = logout_time * 60000 ; // convert minutes to milliseconds
disconnect_page = url_server + disconnect_page ;
page_timeout = window.setTimeout( disconnect, disconnect_time ) ;
}

function reboot_timeOut( logout_time )
{
clearTimeout( page_timeout ) ;
let disconnect_time = logout_time * 60000 ; // convert minutes to milliseconds
page_timeout = window.setTimeout( disconnect, disconnect_time ) ;
}

function disconnect() 
{
location.href = disconnect_page ;
}

function calc( ref_ana, id_res, num_var )
{
console.log("DEBUG calc ref_ana=" + ref_ana + " | id_res=" + id_res + " | num_var=" + num_var) ;

    // search formula for this var
    $(".formula-" + ref_ana ).each( function(i, elem)
    {
    let id_tot   = $(this).attr("id").substr(8) ; 
    let f1 = $(this).val() ;
    let f2 = "" ;

        // Test if exist
        if ( $("#formula2_" + id_tot).length )
        f2 = $("#formula2_" + id_tot).val() ;

    console.log("DEBUG calc id_tot=" + id_tot + " | formula=" + f1 + " | formula2=" + f2) ;

    let formula = f1 ;

        if ( f2 != "" )
        formula = f2 ;

        if ( formula.search("_"+num_var) >= 0 )
        {
        console.log("DEBUG calc num_var found in formula") ;

        // GET current value for all var in this formula
        // TODO if num var greater than 9 ???
        let l_var = [] ;
        
            // Get var number for this formula
            for ( i = 0; i < formula.length; i++ )
            {
            let i_var = formula.indexOf("_", i) + 1 ;

                if ( i_var >= 0 )
                {
                l_var.push( formula.substr(i_var, 1) ) ;

                i = i_var + 1 ;
                }
            }

         let l_value = [] ;

            // Get id_res for each var
            for ( i = 0; i < l_var.length; i++ )
            {
            let id_res_var = $("#num_var_" + ref_ana + "_" + l_var[i] ).attr("class") ;

            let val = $("#res_" + id_res_var ).val() ;

            // TODO if f2 then convert val
                
                if ( val != "" )
                l_value.push( val ) ;
            }
        
         console.log("DEBUG l_var="+l_var) ;
         console.log("DEBUG l_value="+l_value) ;

            // Calculation
            if ( l_var.length == l_value.length )
            {
                for ( i = 0; i < l_var.length; i++ )
                {
                formula = formula.replace("$_"+l_var[i], l_value[i]) ;
                }

            let total = eval(formula) ;

            console.log("DEBUG total="+total) ;
            $("#res_"+id_tot).val(total) ;
            }
        }
    } ) ;
}
