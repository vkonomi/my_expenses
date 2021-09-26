$('#add_to_list').on('click', function() {

    tr_ctg = $("#i_sub_assoc_pr_ctg option:selected").val();
    tr_subctg = $("#i_sub_subctg option:selected").val();
    tr_item = $("#item_name option:selected").val();
    tr_item_name = $("#item_name option:selected").text();
    tr_item_value = $("#tr_item_value").val();

    var tableRef = document.getElementById("pending_items").getElementsByTagName('tbody')[0];
    var newRow = tableRef.insertRow(tableRef.rows.length);
    var cell1 = newRow.insertCell(0);
    var cell2 = newRow.insertCell(1);
    cell1.innerHTML = tr_item_name;
    cell2.innerHTML = tr_item_value;


    $.getJSON('http://localhost:5000/_handle_pending_expense', {
        
        a: tr_ctg,  
        b: tr_subctg, 
        d: tr_item,
        e: tr_item_value

    }, function(data) {
        $.each(data, function(name, value) {
            document.getElementById("tr_total_value").value = value;
        }); 
    });
    $("#i_sub_subctg").empty();
    $("#item_name").empty();
    document.getElementById("tr_item_value").value = 0;

});
