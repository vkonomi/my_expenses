$( document ).ready(function() {

    tr_type = $("#last_tr_type option:selected").val();
    tr_range = $("#last_tr_range option:selected").val();
    //$("#i_sub_subctg").empty();
    $('#last_transactions').DataTable({
            ajax: '/_show_last_transactions',
            columns: [
            {data: 'trans_id', orderable: false, searchable: false},
            {data: 'trans_descr', searchable: false},
            {data: 'trans_type', orderable: false, searchable: false},
            {data: 'trans_total_value', orderable: false, searchable: false},
            {data: 'trans_exec_date'}
            ],
            retrieve: true,
        });




/*
    $.getJSON('http://localhost:5000/_show_last_transactions', {
        
        a: tr_type,  
        b: tr_range, 

    }, function(data) {
        var tableRef = document.getElementById("last_transactions").getElementsByTagName('tbody')[0];
        if (tableRef.rows.length == 0){
            $.each(data, function(id, descr, type, value, date) {
                console.log(id, descr)
                var newRow = tableRef.insertRow(tableRef.rows.length);
                var cell1 = newRow.insertCell(0);
                var cell2 = newRow.insertCell(1);
                var cell3 = newRow.insertCell(2);
                var cell4 = newRow.insertCell(3);
                var cell5 = newRow.insertCell(4);
                cell1.innerHTML = id;
                cell2.innerHTML = descr;
                cell3.innerHTML = type;
                cell4.innerHTML = value;
                cell5.innerHTML = date;
            })
        }
    });

*/
});
