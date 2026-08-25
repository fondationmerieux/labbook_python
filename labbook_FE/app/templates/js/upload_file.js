{#
    Sends the file picked in the #<type_ref> input to the back end, then resolves.
    Returns a promise so the caller can chain on the upload being finished.
#}
function upload_file(type_ref, ref)
{
let param_form = new FormData() ;
let input_file = $('#' + type_ref)[0] ;

    // TEST if an file is waiting
    if (input_file.files.length > 0)
    {
    console.log( "1 file to upload ") ;

    param_form.append('file', input_file.files[0]) ;

        return new Promise(function (resolve, reject)
        {
        console.log( "new promise for " + type_ref ) ;

            $.ajax(
            {
                type : 'POST',
                url : "{{ session['server_ext'] }}/upload-file/" + type_ref + "/" + ref,
                dataType: 'json',
                contentType: false,
                processData: false,
                data: param_form,
                headers: { 'Authorization': 'Bearer {{ session.get("be_access_token","") }}' },
                success : function(response)
                {
                console.log( "success upload ") ;

                resolve(response) ;
                },
                error: function(response)
                {
                console.log("ERROR upload file") ;

                    $("#dial-wait").modal("hide") ;

                alert("{{ _("Une erreur est survenue lors du dépot d'un fichier") }}") ;

                reject(response) ;
                }
            } ) ;
        } ) ;
    }
    else
    {
    console.log( "file empty upload ") ;

        return new Promise(function (resolve, reject) { resolve(true) } ) ;
    }
}
