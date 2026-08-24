{#
    Renders one analysis in the search dropdown: code, name and family.
#}
function formatRepoAnalysis(repo)
{
    if (repo.loading)
        return repo.text ;

    var code = "" ;

    if (repo.code)
        code += "[" + repo.code + "]" ;

    var name = "" ;

    if (repo.name)
        name += repo.name ;

    var cat = "" ;

    if (repo.label)
        cat += repo.label ;

    var display = $(
        "<div class='select2-result-repository clearfix'>" +
        "<div class='select2-result-repository__meta'>" +
        "<div class='select2-result-repository__code'><b>" + code + "</b></div>" +
        "<div class='select2-result-repository__name'>" + name + "</div>" +
        "<div class='select2-result-repository__category'>" + cat + "</div>" +
        "</div>" +
        "</div>") ;

    return display ;
}
