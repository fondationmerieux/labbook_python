/* javascript functions for labbook project */
var disconnect_page = "/sigl/disconnect" ;
var page_timeout    = 0 ;

function tempAlert(msg, id_elem)
{
let w_page  = $("#page").width() / 2 - 80 ; // -80 for better center

let pos_elem = $("#" +id_elem).position();
let x = pos_elem.left;
let y = pos_elem.top - 80; // -80 for raise up a bit

if ( y < 120 ) y = 120 ; // less than 100 it's non visible beacuse hide by menu

$(".toast").css({ top: y }) ;
$(".toast").css({ left: w_page + 'px' }) ;

$("#toast-msg").html(msg) ;

$(".toast").toast('show') ;
}

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

function status_rec( id_stat, with_det )
{
let res = '' ;

    if ( id_stat == 182 )
    res = '<span class="icon stat-A">A</span>' ;
    else if ( id_stat == 253 )
    res = '<span class="icon stat-A">I</span>' ;
    else if ( id_stat == 254 )
    res = '<span class="icon stat-T">T</span>' ;
    else if ( id_stat == 255 )
    res = '<span class="icon stat-T">I</span>' ;
    else if ( id_stat == 256 )
    res = '<span class="icon stat-B">B</span>' ;

return res ;
}

function status_res( id_stat )
{
let res = '' ;

    if ( id_stat == 250 )
    res = '<span class="icon stat-A">A</span>' ;
    else if ( id_stat == 251 )
    res = '<span class="icon stat-T">T</span>' ;
    else if ( id_stat == 252 )
    res = '<span class="icon stat-B">B</span>' ;

return res ;
}

function emer( flag_emer )
{
let res = '' ;

    if ( flag_emer == "O" || flag_emer == 4 )
    res = '<span class="emer">&nbsp;</span>' ;

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

function calc( id_rec, ref_ana, id_res, num_var )
{
//console.log("####################### DEBUG CALC ###################");
//console.log("DEBUG ref_ana=" + ref_ana + " | id_res=" + id_res + " | num_var=" + num_var) ;

// start by evaluate this var
eval_value( id_rec, ref_ana, id_res ) ;

    // search formula for this var
    $(".formula-" + id_rec + "-" + ref_ana ).each( function(i, elem)
    {
    let id_tot  = $(this).attr("id").substr(8) ; 
    let f1      = $(this).val() ;
    let f2      = "" ;

    //console.log("==> DEBUG calc id_tot=" + id_tot );
    //console.log("==> DEBUG calc f1=" + f1 );

        // Test if exist
        if ( $("#formula2_" + id_rec + "-" + id_tot).length )
        f2 = $("#formula2_" + id_rec + "-" + id_tot).val() ;

    //console.log("==> DEBUG calc f2=" + f2 );

        // EVAL f1
        if ( f1.search("_"+num_var) >= 0 )
        {
        //console.log("DEBUG calc num_var found in f1") ;

        // GET current value for all var in this formula
        // NOTE if num var greater than 9 ???
        let l_var   = [] ;
        let k_var_p = 0  ;

            // Get var number for this formula
            for ( k = 0; k < f1.length; k++ )
            {
            let k_var = f1.indexOf("_", k) + 1 ;

                // stop rotate
                if ( k_var <= k_var_p )
                break ;

                if ( k_var >= 0 && k_var < f1.length )
                {
                l_var.push( f1.substr(k_var, 1) ) ;

                k = k_var + 1 ;

                k_var_p = k_var ;
                }
            }

         //console.log("DEBUG f1 l_var="+l_var) ;

         let l_value = [] ;

            // Get id_res for each var
            for ( k = 0; k < l_var.length; k++ )
            {
            let val_tmp = "" ;

                $(".num_var-" + id_rec + "-" + ref_ana + "-" + l_var[k]).each( function(j, elem)
                {
                let id_res_var = $(this).attr("id") ;

                    // if no value we try to getting one
                    if ( val_tmp == null || val_tmp == "" )
                    {
                    val_tmp = $("#res_"+id_res_var).val() ;

                        if ( val_tmp != null && val_tmp != "" )
                        {
                        l_value.push( val_tmp ) ;
                        }
                    }

                } ) ;
            }
        
         //console.log("DEBUG f1 l_value="+l_value) ;

            // Calculation
            if ( l_var.length == l_value.length )
            {
                for ( k = 0; k < l_var.length; k++ )
                {
                f1 = f1.replace("$_"+l_var[k], l_value[k]) ;
                }

            //console.log("DEBUG formule f1 avant eval : " + f1);
            let total = eval(f1) ;

            //console.log("DEBUG TOTAL VIA f1="+total) ;
            let accu = $("#accu_"+id_tot).val() ;

                if ( accu == null || accu == "" )
                accu = 2 ;

            //console.log("DEBUG #res_" + id_tot + " = " + Number(total).toFixed( accu ) ) ;

            $("#res_"+id_tot).val( Number(total).toFixed( accu ) ) ;
            }
        }

        // EVAL f2 if no result with f1
        if ( f2 != "" && $("#res_"+id_tot).val() != null && f2.search("_"+num_var) >= 0 )
        {
        //console.log("DEBUG calc num_var found in f2") ;

        // GET current value for all var in this formula
        // NOTE if num var greater than 9 ???
        let l_var   = [] ;
        let k_var_p = 0  ;

            // Get var number for this formula
            for ( k = 0; k < f2.length; k++ )
            {
            let k_var = f2.indexOf("_", k) + 1 ;

                // stop rotate
                if ( k_var <= k_var_p )
                break ;

                if ( k_var >= 0 && k_var < f2.length )
                {
                l_var.push( f2.substr(k_var, 1) ) ;

                k = k_var + 1 ;

                k_var_p = k_var ;
                }
            }

         //console.log("DEBUG f2 l_var="+l_var) ;

         let l_value = [] ;

            // Get id_res for each var of same unit
            for ( k = 0; k < l_var.length; k++ )
            {
            let val_tmp = "" ;

                $(".num_var-" + id_rec + "-" + ref_ana + "-" + l_var[k]).each( function(j, elem)
                {
                let id_res_var = $(this).attr("id") ;

                    // if no value we try to getting one
                    if ( val_tmp == null || val_tmp == "" )
                    {
                    val_tmp = $("#res2_" + id_res_var ).val() ;
                   
                        if ( val_tmp != null && val_tmp != "" )
                        {
                        l_value.push( val_tmp ) ;
                        }
                    }

                } ) ;
            }
        
         //console.log("DEBUG f2 l_value="+l_value) ;

            // Calculation
            if ( l_var.length == l_value.length )
            {
                for ( k = 0; k < l_var.length; k++ )
                {
                f2 = f2.replace("$_"+l_var[k], l_value[k]) ;
                }

            let total = eval(f2) ;

            //console.log("DEBUG TOTAL VIA f2="+total) ;
                if ( $("#res_"+id_tot).val() == null || $("#res_"+id_tot).val() == "")
                {
                let accu = $("#accu_"+id_tot).val() ;

                    if ( accu == null || accu == "" )
                    accu = 2 ;

                $("#res_"+id_tot).val( Number(total).toFixed( accu )) ;
                $("#res2_"+id_tot).val(total) ;
                }
            
            }
        }
    } ) ;
}

function eval_value( id_rec, ref_ana, id_res )
{
//console.log("DEBUG EVAL_VALUE -------------------------------------");
let val  = $( "#res_"+id_res ).val()  ;
let val2 = "" ; 
let f2   = "" ;

    if ( val == null || val == "" )
    return "";

    // Test if a formula exist attached to this result
    if ( $("#formula2_" + id_rec + "-" + id_res).length )
    {
    f2 = $("#formula2_" + id_rec + "-" + id_res).val() ;

    // NOTE if num var greater than 9 ???
    let l_var   = [] ;
    let i_var_p = 0 ;

        // Get var number for this formula
        for ( i = 0; i < f2.length; i++ )
        {
        let i_var = f2.indexOf("_", i) + 1 ;

            // stop rotate
            if ( i_var <= i_var_p )
            break ;

            if ( i_var >= 0 )
            {
            l_var.push( f2.substr(i_var, 1) ) ;

            i = i_var + 1 ;

            i_var_p = i_var ;
            }
        }

    //console.log("EVAL_VALUE l_var="+l_var) ;

    let l_value = [] ;

        // Get id_res for each var
        for ( i = 0; i < l_var.length; i++ )
        {
        let val_tmp = "" ;    

            $(".num_var-" + ref_ana + "-" + l_var[i]).each( function(j, elem)
            {
            let id_res_var = $(this).attr("id") ;

                // if no value we try to getting one
                if ( val_tmp == null || val_tmp == "" )
                {
                    // value in calculation
                    if ( id_res_var == id_res )
                    val_tmp = val ;
                    // convert value
                    else
                    val_tmp = $("#res2_" + id_res_var ).val() ;
             
                    if ( val_tmp != null && val_tmp != "" )
                    l_value.push( val ) ;
                }

            } ) ;
        }

    //console.log("EVAL_VALUE l_value="+l_value) ;

        // Calculation
        if ( l_var.length == l_value.length )
        {
            for ( i = 0; i < l_var.length; i++ )
            {
            f2 = f2.replace("$_"+l_var[i], l_value[i]) ;
            }

        let total = eval(f2) ;

        //console.log("DEBUG EVAL_VALUE total2="+total) ;
        $("#res2_"+id_res).val(total) ;
        }
        else
        $("#res2_"+id_res).val("") ;
    }
    else
    $("#res2_"+id_res).val(val) ;
 
//console.log("------------------------------------------------------");
}
