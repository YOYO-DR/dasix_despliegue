$(function(){
    $('#data').DataTable({
        responsive: true, 
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathnam,
            type: 'POST',
            data: {'action': 'searchdata'}, // parametros
            dataSrc: ""
        },
        columns: [
            { "data": "id"},
            { "data": "Nombre"},
            { "data": "Descripcion"},
            { "data": "Descripcion"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons =
                      '<a  href="/categoria/update/' +
                      row.id +
                      '/" class="btn btn-primary btn-s btn-flat btn-bg-morado-2"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/categoria/delete/'+row.id+'/" type="button" class="btn btn-danger btn-s btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function(settings, json) {

          }
        });
})