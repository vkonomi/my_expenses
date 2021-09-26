$('#i_sub_subctg').on('click', function() {

    sctg_name = $("#i_sub_subctg option:selected").text();
    sctg_id = $("#i_sub_subctg option:selected").val();
    $("#item_name").empty();
    console.log(sctg_name)
        
    $.getJSON('http://localhost:5000/_get_items', {
        
        b: sctg_id,
        a: sctg_name

    }, function(data) {
        
        console.log(data)
        var options = $("#item_name");
        $.each(data, function(key, value) {
            options.append($("<option></option>").val(key).text(value))
        }); 
    });
});