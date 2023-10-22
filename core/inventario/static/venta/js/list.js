var tblVenta; // inicializar la varible que tendra el elemento de la tabla

$(function () {
  // que se ejecute cuando cargue el html

  tblVenta = $("#data").DataTable({
    // le agrego el datatable
    responsive: true, // que sea responsivo
    autoWidth: false, // que no moleste los width predeterminados en la tabla
    destroy: true, // que se pueda eliminar valores
    deferRender: true, //trabaje de forma optima con demasiados datos
    ajax: {
      // la peticion para pedir los datos
      url: window.location.pathname, // pedirlos a la vista actual
      type: "POST",
      data: {
        //datos para pedir los registros
        action: "searchdata",
      },
      dataSrc: "",
    },
    columns: [
      //indicando las columnas que vienen en los datos
      { data: "id" },
      { data: "Cli.Nombres" },
      { data: "Date_joined" },
      { data: "Subtotal" },
      { data: "Iva" },
      { data: "Total" },
      { data: "id" }, // repito este porque voy a modificarlo
    ],
    columnDefs: [
      {
        targets: [-2, -3, -4], // posiciones de los "columns"
        class: "text-center", // le pongo esta clase
        orderable: false, // que no se pueda ordenar por estas columnas
        render: function (data, type, row) {
          return "$" + parseFloat(data).toFixed(2); // los datos lo retorna como "$5.00"
        },
      },
      {
        targets: [-1], // seleccionar la ultima columna
        class: "text-center",
        orderable: false, // que no se ordene
        render: function (data, type, row) {
          // creo los botones de actualizar y eliminar
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
  $("#data tbody") // seleccionar el body de la tabla
    .on("click", 'a[rel="detalle"]', function () {
      // agregar el evento click a los los links de detalle
      var tr = tblVenta.cell($(this).closest("td, li")).index(); // obtener toda la fila
      var data = tblVenta.row(tr.row).data(); // obtener la info de la fila
      $("#tblDet").DataTable({
        //seleccionar la tabla del modal y poner los datos
        responsive: true, // que sea responsiva
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
          // pedir los datos
          url: window.location.pathname,
          type: "POST",
          data: {
            // buscar los datos de la venta, por el id de la venta
            action: "search_detalle_produ",
            id: data.id,
          },
          dataSrc: "",
        },
        columns: [
          //columnas
          { data: "Produ.Nombre" },
          { data: "Produ.cate.Nombre" },
          { data: "Precio" },
          { data: "Cantidad" },
          { data: "Subtotal" },
        ],
        columnDefs: [
          {
            // seleccionar las columnas y cambiar la forma en como se ve
            targets: [-1, -3],
            class: "text-center",
            render: function (data, type, row) {
              return "$" + parseFloat(data).toFixed(2);
            },
          },
          {
            targets: [-2],
            class: "text-center",
            render: function (data, type, row) {
              return data;
            },
          },
        ],
        initComplete: function (settings, json) {},
      });
      $("#myModelDet").modal("show"); //mostrar el modal
    });
});
