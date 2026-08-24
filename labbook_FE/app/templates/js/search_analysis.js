{#
    Analysis search field (select2) shared by the result and validation pages.
    Expects an element #search_analysis and the formatRepoAnalysis function.
#}
$("#search_analysis").select2(
    {
        placeholder: "{{ _("Cliquer pour commencer une recherche") }}",
        tags: false,
        multiple: false,
        tokenSeparators: [','],
        minimumInputLength: 2,
        ajax: {
            url: "{{ session['server_ext'] }}/services/analysis/search/A",
            type: "POST",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            term: $("#search_analysis").text(),
            headers: { 'Authorization': 'Bearer {{ session.get("be_access_token","") }}' },
            data: function (params) {
                return JSON.stringify(
                    {
                        term: params.term,
                        link_fam: {{ session['user_link_fam'] or [] }}
                    } ) ;
            },
            processResults: function (data) {
                return {
                    // data need id key if not no focus selection displayed
                    results: data
                } ;
            }
        },
        templateResult: formatRepoAnalysis
    } ) ;
