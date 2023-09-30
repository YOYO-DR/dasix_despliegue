var tblVenta;

$(function () {

    tblVenta = $("#data").DataTable({
      responsive: true,
      autoWidth: false,
      destroy: true,
      deferRender: true,
      ajax: {
        url: window.location.pathname,
        type: "POST",
        data: {
          action: "searchdata",
        },
        dataSrc: "",
      },
      columns: [
        {data: "id"},
        { data: "Cli.Nombres" },
        { data: "Date_joined" },
        { data: "Subtotal" },
        { data: "Iva" },
        { data: "Total" },
        { data: "id" },
      ],
      columnDefs: [
        {
          targets: [-2, -3, -4],
          class: "text-center",
          orderable: false,
          render: function (data, type, row) {
            return "$" + parseFloat(data).toFixed(2);
          },
        },
        {
          targets: [-1],
          class: "text-center",
          orderable: false,
          render: function (data, type, row) {
            var buttons =
              '<a href="/venta/delete/' +
              row.id +
              '/" class="btn btn-danger btn-s btn-flat"><i class="fas fa-trash-alt"></i></a> ';
            buttons +=
              '<a href="/venta/update/' +
              row.id +
              '/" class="btn btn-primary btn-s btn-flat btn-bg-morado-2"><i class="fas fa-edit"></i></a> ';
            buttons +=
              '<a rel="detalle" class="btn btn-success btn-s btn-flat text-white"><i class="fas fa-search"></i></a> ';
            return buttons;
          },
        },
      ],
      initComplete: function (settings, json) {},
    });

    $('#data tbody')
        .on('click', 'a[rel="detalle"]', function () {
            var tr = tblVenta.cell($(this).closest('td, li')).index();
            var data = tblVenta.row(tr.row).data();

            $('#tblDet').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                //data: data.det,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_detalle_produ',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "Produ.Nombre"},
                    {"data": "Produ.cate.Nombre"},
                    {"data": "Precio"},
                    {"data": "Cantidad"},
                    {"data": "Subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [-1, -3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#myModelDet').modal('show');
        });
});