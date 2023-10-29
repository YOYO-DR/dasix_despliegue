//obtener el elemento de donde se llama el script
const scriptElement = document.currentScript;

//obtengo el valor de la url que la paso por la data del script
const urlList = scriptElement.getAttribute("data-url-list");

var tblProductos; //inicializar la variable del datatable

var ventas = {
  // Inicializamos los valores de una venta
  iva_por: 0.19, // Valor de iva predeterminado
  items: {
    Cli: "", //cliente
    Date_joined: "", //fecha de creacion
    Subtotal: 0.0,
    Iva: 0.0,
    Total: 0.0,
    productos: [], // detalles de venta (detalleVenta)
  },
  // obtener los ids de cada producto
  get_ids: function () {
    var ids = [];
    //el this hace referencia al contexto actual, en este caso es la variable "ventas" por eso desde el this puedo acceder a los items
    $.each(this.items.productos, function (key, value) {
      // con push agrego el id del producto a la lista de ids
      ids.push(value.id);
    });
    return ids;
  },

  calcular_factura: function () {
    var Subtotal = 0.0;
    //obtenemos el iva del input
    var iva = $('input[name="Iva"]').val();
    //se convierte en decimal (float)
    iva = parseFloat(iva);
    
    //se recorre cada detalle de venta y obtenemos su total multiplicando la cantidad por su valor y lo vamos guardando en la variable subtotal porque ese sera el subtotal de toda la venta
    $.each(this.items.productos, function (pos, dict) {
      dict.Subtotal = dict.Cantidad * parseFloat(dict.pvp);
      Subtotal += dict.Subtotal;
    });

    this.items.Subtotal = Subtotal; // se lo asignamos a al subtotal de la venta
    this.items.Iva = this.items.Subtotal * iva; //obtenemos el valor del iva multiplicando el subtotal por el porcentaje del iva ingresado
    this.items.Total = this.items.Subtotal + this.items.Iva; // obtenemos el total que es el subtotal por el iva

    // asignamos los valores a los inputs
    $('input[name="Subtotal"]').val(this.items.Subtotal.toFixed(2)); // subtotal
    $('input[name="ivacalc"]').val(this.items.Iva.toFixed(2)); //iva calculado
    $('input[name="Total"]').val(this.items.Total.toFixed(2)); //total
  },

  // esta funcion es para agregar los detalle de venta/productos a la lista de productos
  add: function (item) {
    this.items.productos.push(item);
    //actualizamos la tabla
    this.list();
  },

  list: function () {
    //se calcula la factura inicial o si tienes datos, con los datos actuales
    this.calcular_factura();
    // se genera/actualiza la tabla de datatable
    tblProductos = $("#tblProductos").DataTable({
      responsive: true,
      autoWidth: false,
      destroy: true,
      data: this.items.productos, // le paso la data con la que trabaja, que son los productos de la venta
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
          targets: [-4], // personalizo el stock
          class: "text-center", //centro texto
          orderable: false, // si se puede ordenar por esta columna
          render: function (data, type, row) { // retorno como se va a ver el valor en la tabla
            return '<span class="badge badge-secondary">' + data + "</span>";
          },
        },
        {
          targets: [0], // personalizo el id
          class: "text-center",
          orderable: false,
          render: function (data, type, row) { // Utilizo esta columna para poner el boton de eliminar
            return '<a rel="remove" class="btn btn-danger btn-s btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
          },
        },
        {
          targets: [-3], // personalizo el valor de pvp
          class: "text-center",
          orderable: false,
          render: function (data, type, row) {
            return "$" + parseFloat(data).toFixed(2); // lo convierto en decimal y le digo que tenga 2 decimales y le concateno el $
          },
        },
        {
          targets: [-2], // personalizo la cantidad
          class: "text-center",
          orderable: false,
          render: function (data, type, row) {
            return (// lo convierto en un input para modificar la cantidad
              '<input type="text" name="cant" class="form-control form-control-sm input-sm"  autocomplete="off" value="' +
              row.Cantidad +
              '">'
            );
          },
        },
        {
          targets: [-1],// personalizo el subtotal
          class: "text-center",
          orderable: false,
          render: function (data, type, row) {
            return "$" + parseFloat(data).toFixed(2);
          },
        },
      ],

      // esta funcion "rowCallback" me permite modificar algunos valores de la tabla a medida que se vaya creando nuevos registros en mi tabla
      rowCallback(row, data, displayNum, displayIndex, dataIndex) {
        // accedo al input de cantidad
        $(row).find('input[name="cant"]').TouchSpin({ // libreria para el input numerico, para lo botones de + y -
          min: 1, // minimo valor
          max: data.Stock, // maximo valor - el cual es el stock del producto
          step: 1, // valor de incremento o decremento
        });
      },
      // funcion que se ejecuta cuando se carga la tabla completa
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

// funcion principal que se ejecuta cuando cargue el html
$(function () {
  $(".select2").select2({ // seleccionar el select y convertirlo con la libreria de select2
    theme: "bootstrap4",
    language: "es",
  });

  $("#Date_joined").datetimepicker({ // seleccionar el input de fecha y formatearlo con datetimepicker
    format: "YYYY-MM-DD",
    defaultDate: moment().format("YYYY-MM-DD"),
    locale: "es",
  });

  $("input[name='Iva']") // le aplico el TouchSpin
    .TouchSpin({
      min: 0,
      max: 1,
      step: 0.01,
      decimals: 2, //decimales
      boostat: 5,
      maxboostedstep: 10,
      postfix: "%",
    })
    .on("change", function () {
      ventas.calcular_factura(); // cuando se cambien el numero del input
    })
    .val(ventas.iva_por); //le pongo el valor del iva predeterminado

  $(".btnRemoveAll").on("click", function () {
    // btn de borrar todo, en su evento click
    // si los proudctos esta vacion, no hago nada
    if (ventas.items.productos.length == 0) return false;
    alert_action( // utilizo una alerta de confirmacion
      "Notificacion",
      "¿Estas seguro de eliminar todos los items de tu detalle?",
      function () { // funcion a ejecutar si dice que si
        ventas.items.productos = []; // limpio los productos
        ventas.list(); // actualizo la tabla
      }
    );
  });

  // evento de cantidad
  $("#tblProductos tbody")
    .on("click", 'a[rel="remove"]', function () {// agrego el evento click al btn de eliminar
      var tr = tblProductos.cell($(this).closest("td, li")).index(); // obtener el tr actual
      alert_action(
        "Notificacion",
        "¿Estas seguro de eliminar el producto de tu detalle?",
        function () {
          ventas.items.productos.splice(tr.row, 1); // quito la row de la venta
          ventas.list(); // actualizo la tabla
        }
      );
    })
    .on("change keyup", 'input[name="cant"]', function () { // evento de escribir en el input de la cantidad
      var cant = parseInt($(this).val()); //obtengo la cantidad y la convierto a entero
      var tr = tblProductos.cell($(this).closest("td, li")).index(); // obtengo la fila actual

      ventas.items.productos[tr.row].Cantidad = cant; // modifico la cantidad en el arreglo en productos
      ventas.calcular_factura();// calculo la factura
      $("td:eq(5)", tblProductos.row(tr.row).node()).html( //accedo al subtotal y cambio el valor 
        "$" + ventas.items.productos[tr.row].Subtotal.toFixed(2)
      );
    });

  //evento del submit
  $("form").on("submit", function (e) {
    e.preventDefault();// detengo el evento del form
    if (ventas.items.productos.length == 0) { // verifico que tenga productos
      message_error("Debe tener al menos un item en su detalle de venta");
      return false;
    }
    ventas.items.Date_joined = $('input[name="Date_joined"]').val(); // obtengo la fecha
    ventas.items.Cli = $('select[name="Cli"]').val(); // obtengo el cliente
    var parametros = new FormData(); // inicializo los parametros
    parametros.append("action", $('input[name="action"]').val()); //agrego la accion
    parametros.append("ventas", JSON.stringify(ventas.items));//agrego los items de la venta
    submit_with_ajax(
      //envio la peticion y si es correcto lo redirecciono a la lista de ventas
      window.location.pathname,
      "Guardar",
      "¿Quiere realizar esta accion?",
      parametros,
      function () {
        location.href = urlList;
      }
    );
  });

  //Inicializa el datatable con los valores que tenga o vacio
  ventas.list();

  $('select[name="search"]') // select para buscar
    .select2({
      theme: "bootstrap4",
      language: "es",
      allowClear: true,
      ajax: { // esto es para que cada vez que busque se envie la peticion
        delay: 250,
        type: "POST",
        url: window.location.pathname,
        data: function (params) {
          var queryParametros = {
            term: params.term, // palabra escrita
            action: "search-productos", // accion
            ids: JSON.stringify(ventas.get_ids()), //estos ids son de los productos que ya estan en la tabla, asi que esos no los buscara o mostrara en el resultado de busqueda
          };
          return queryParametros;
        },
        // procesar los datos recibidos
        processResults: function (data) {
          return {
            results: data,
          };
        },
      },
      placeholder: "Ingrese una descripcion",
      minimumInputLength: 1, // minima letra para buscar
      templateResult: formatRepo, // le paso la funcion que creara la vista de resultado
    })
    .on("select2:select", function (e) { //evento cuando seleccione un elemento
      var data = e.params.data;
      data.Cantidad = 1;
      data.Subtotal = 0.0;
      ventas.add(data); // agrego los datos a la venta
      $(this).val("").trigger("change.select2"); // limpio el input
    });
});
