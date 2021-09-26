$('#i_sub_assoc_pr_ctg').on('click', function() {

    ctg_name = $("#i_sub_assoc_pr_ctg option:selected").text();
    ctg_id = $("#i_sub_assoc_pr_ctg option:selected").val();
    $("#i_sub_subctg").empty();
        
    $.getJSON('http://localhost:5000/_get_subcategories', {
        
        b: ctg_id,
        a: ctg_name

    }, function(data) {
        
        console.log(data)
        var options = $("#i_sub_subctg");
        $.each(data, function(key, value) {
            console.log(key, value)
            options.append($("<option></option>").val(key).text(value))
        }); 
    });
});
