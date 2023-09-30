$(function () {
    const data_table=$('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "Nombre"},
            {"data": "cate.Nombre"},
            {"data": "image"},
            {"data": "Stock"},
            {"data": "pvp"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<button class="btn btn-img-info"><img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;"></button>';
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if(data>0){
                        return '<span class="badge badge-success">'+data+'</span'
                    }

                    return '<span class="badge badge-danger">'+data+'</span'
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$'+parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons =
                      '<a href="/producto/update/' +
                      row.id +
                      '/" class="btn btn-primary btn-s btn-flat btn-bg-morado-2"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/producto/delete/' + row.id + '/" type="button" class="btn btn-danger btn-s btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
      initComplete: function (settings, json) {
        //poner evento a los botones de la imagen de cada producto
        $("#data").on("click", ".btn-img-info", function () {
          let fila = $(this).closest("tr, li")
          let data = data_table.row(fila).data();
          $("#modal-img .modal-title b").html(`<i class="far fa-image"></i> Imagen del producto <i>${data.Nombre}</i>`)
          $("#modal-img .modal-body").html(`<img class="img-fluid" src="${data.image}">`);
          $("#modal-img").modal("show");
        })
        }
    });
});