$('#income_subcat').on('click', function() {

    i_sctg_name = $("#income_subcat option:selected").text();
    i_sctg_id = $("#income_subcat option:selected").val();
    $("#income_item").empty();
        
    $.getJSON('http://localhost:5000/_get_items', {
        
        b: i_sctg_id,
        a: i_sctg_name

    }, function(data) {
        
        console.log(data)
        var options = $("#income_item");
        $.each(data, function(key, value) {
            options.append($("<option></option>").val(key).text(value))
        }); 
    });
});
