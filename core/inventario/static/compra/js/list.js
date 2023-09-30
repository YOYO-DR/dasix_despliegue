$(function () {
    const data_table = $("#data").DataTable({
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
        { data: "id" },
        { data: "Proveedor" },
        { data: "Producto.Nombre" },
        { data: "Producto.Precio" },
        { data: "Cantidad" },
        { data: "id" },
      ],
      columnDefs: [
        {
          targets: [-3],
          class: "text-center",
          render: function (data, type, row) { 
            return `$${data}`
          }
        },
        {
          targets: [-1],
          class: "text-center",
          orderable: false,
          render: function (data, type, row) {
            var buttons =
              '<a href="/compra/update/' +
              row.id +
              '/" class="btn btn-primary btn-s btn-flat btn-bg-morado-2"><i class="fas fa-edit"></i></a> ';
            buttons +=
              '<a href="/compra/delete/' +
              row.id +
              '/" type="button" class="btn btn-danger btn-s btn-flat"><i class="fas fa-trash-alt"></i></a>';
            return buttons;
          },
        },
      ],
      initComplete: function (settings, json) {},
    });
});