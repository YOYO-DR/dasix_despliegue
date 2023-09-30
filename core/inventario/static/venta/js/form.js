//obtener el script
const scriptElement = document.currentScript;

//obtengo los valores de data
const urlList = scriptElement.getAttribute("data-url-list");

var tblProductos;
var ventas = {
  iva_por: 0.12,
  items: {
    Cli: "",
    Date_joined: "",
    Subtotal: 0.0,
    Iva: 0.0,
    Total: 0.0,
    productos: [],
  },
  get_ids: function () {
    var ids = [];
    $.each(this.items.productos, function (key, value) {
      ids.push(value.id);
    });
    return ids;
  },

  calcular_factura: function () {
    var Subtotal = 0.0;
    var iva = $('input[name="Iva"]').val();
    iva = parseFloat(iva);
    $.each(this.items.productos, function (pos, dict) {
      dict.Subtotal = dict.Cantidad * parseFloat(dict.pvp);
      Subtotal += dict.Subtotal;
    });

    this.items.Subtotal = Subtotal;
    this.items.Iva = this.items.Subtotal * iva;
    this.items.Total = this.items.Subtotal + this.items.Iva;
    $('input[name="Subtotal"]').val(this.items.Subtotal.toFixed(2));
    $('input[name="ivacalc"]').val(this.items.Iva.toFixed(2));
    $('input[name="Total"]').val(this.items.Total.toFixed(2));
  },
  add: function (item) {
    this.items.productos.push(item);
    this.list();
  },
  list: function () {
    this.calcular_factura();
    tblProductos = $("#tblProductos").DataTable({
      responsive: true,
      autoWidth: false,
      destroy: true,
      data: this.items.productos,
      columns: [
        { data: "id" },
        { data: "full_nombre" },
        { data: "Stock" },
        { data: "pvp" },
        { data: "cant" },
        { data: "Subtotal" },
      ],
      columnDefs: [
        {
          targets: [-4],
          class: "text-center",
          orderable: false,
          render: function (data, type, row) {
            return '<span class="badge badge-secondary">' + data + "</span>";
          },
        },
        {
          targets: [0],
          class: "text-center",
          orderable: false,
          render: function (data, type, row) {
            return '<a rel="remove" class="btn btn-danger btn-s btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
          },
        },
        {
          targets: [-3],
          class: "text-center",
          orderable: false,
          render: function (data, type, row) {
            return "$" + parseFloat(data).toFixed(2);
          },
        },
        {
          targets: [-2],
          class: "text-center",
          orderable: false,
          render: function (data, type, row) {
            return (
              '<input type="text" name="cant" class="form-control form-control-sm input-sm"  autocomplete="off" value="' +
              row.Cantidad +
              '">'
            );
          },
        },
        {
          targets: [-1],
          class: "text-center",
          orderable: false,
          render: function (data, type, row) {
            return "$" + parseFloat(data).toFixed(2);
          },
        },
      ],

      // esta funcion "rowCallback" me permite modificar algunos valores de la tabla a medida que se vaya creando nuevos registros en mi tabla
      rowCallback(row, data, displayNum, displayIndex, dataIndex) {
        $(row).find('input[name="cant"]').TouchSpin({
          min: 1,
          max: data.Stock,
          step: 1,
        });
      },
      initComplete: function (settings, json) {},
    });
  },
};

function formatRepo(repo) {
  if (repo.loading) {
    return repo.text;
  }

  var option = $(
    '<div class="wrapper container">' +
      '<div class="row">' +
      '<div class="col-sm-3 col-lg-2">' +
      '<img src="' +
      repo.image +
      '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
      "</div>" +
      '<div class="col-sm-9 col-lg-10 text-left shadow-sm">' +
      '<p style="margin-bottom: 0;">' +
      "<b>Nombre:</b> " +
      repo.full_nombre +
      "<br>" +
      "<b>Stock:</b> " +
      repo.Stock +
      "<br>" +
      '<b>PVP:</b> <span class="badge badge-warning">$' +
      repo.pvp +
      "</span>" +
      "</p>" +
      "</div>" +
      "</div>" +
      "</div>"
  );

  return option;
}

$(function () {
  $(".select2").select2({
    theme: "bootstrap4",
    language: "es",
  });

  $("#Date_joined").datetimepicker({
    format: "YYYY-MM-DD",
    defaultDate: moment().format("YYYY-MM-DD"),
    locale: "es",
    //minDate: moment().format("YYYY-MM-DD")
  });

  $("input[name='Iva']")
    .TouchSpin({
      min: 0,
      max: 100,
      step: 0.01,
      decimals: 2,
      boostat: 5,
      maxboostedstep: 10,
      postfix: "%",
    })
    .on("change", function () {
      ventas.calcular_factura();
    })
    .val(ventas.iva_por);

  $(".btnRemoveAll").on("click", function () {
    if (ventas.items.productos.length == 0) return false;
    alert_action(
      "Notificacion",
      "¿Estas seguro de eliminar todos los items de tu detalle?",
      function () {
        ventas.items.productos = [];
        ventas.list();
      }
    );
  });

  // evento de cantidad
  $("#tblProductos tbody")
    .on("click", 'a[rel="remove"]', function () {
      var tr = tblProductos.cell($(this).closest("td, li")).index();
      alert_action(
        "Notificacion",
        "¿Estas seguro de eliminar el producto de tu detalle?",
        function () {
          ventas.items.productos.splice(tr.row, 1);
          ventas.list();
        }
      );
    })
    .on("change keyup", 'input[name="cant"]', function () {
      var cant = parseInt($(this).val());
      var tr = tblProductos.cell($(this).closest("td, li")).index();

      ventas.items.productos[tr.row].Cantidad = cant;
      ventas.calcular_factura();
      $("td:eq(5)", tblProductos.row(tr.row).node()).html(
        "$" + ventas.items.productos[tr.row].Subtotal.toFixed(2)
      );
    });

  //evento del submit
  $("form").on("submit", function (e) {
    e.preventDefault();
    if (ventas.items.productos.length == 0) {
      message_error("Debe tener al menos un item en su detalle de venta");
      return false;
    }
    ventas.items.Date_joined = $('input[name="Date_joined"]').val();
    ventas.items.Cli = $('select[name="Cli"]').val();
    var parametros = new FormData();
    parametros.append("action", $('input[name="action"]').val());
    parametros.append("ventas", JSON.stringify(ventas.items));
    submit_with_ajax(
      window.location.pathname,
      "Guardar",
      "¿Quiere realizar esta accion?",
      parametros,
      function () {
        location.href = urlList;
      }
    );
  });

  ventas.list();

  $('select[name="search"]')
    .select2({
      theme: "bootstrap4",
      language: "es",
      allowClear: true,
      ajax: {
        delay: 250,
        type: "POST",
        url: window.location.pathname,
        data: function (params) {
          var queryParametros = {
            term: params.term,
            action: "search-productos",
            ids: JSON.stringify(ventas.get_ids()),
          };
          return queryParametros;
        },
        processResults: function (data) {
          return {
            results: data,
          };
        },
      },
      placeholder: "Ingrese una descripcion",
      minimumInputLength: 1,
      templateResult: formatRepo,
    })
    .on("select2:select", function (e) {
      var data = e.params.data;
      data.Cantidad = 1;
      data.Subtotal = 0.0;
      ventas.add(data);
      $(this).val("").trigger("change.select2");
    });
});
