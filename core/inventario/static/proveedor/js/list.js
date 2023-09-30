//obtener el script
const scriptElement = document.currentScript;

//obtengo los valores de data
const urlDelete = scriptElement
  .getAttribute("data-url-delete")
  .replace("0/","");
const urlUpdate = scriptElement
  .getAttribute("data-url-update")
  .replace("0/","");

$(function () {
  $("#data").DataTable({
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
      { data: "Nombres" },
      { data: "Identificacion" },
      { data: "Telefono" },
      { data: "Correo" },
      { data: "id" },
    ],
    columnDefs: [
      {
        targets: [-1],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          var buttons =
            '<a href="' + urlUpdate + row.id +
            '/" class="btn btn-primary btn-s btn-flat btn-bg-morado-2"><i class="fas fa-edit"></i></a> ';
          buttons +=
            '<a href="'+urlDelete +
            row.id +
            '/" type="button" class="btn btn-danger btn-s btn-flat"><i class="fas fa-trash-alt"></i></a>';
          return buttons;
        },
      },
    ],
    initComplete: function (settings, json) {},
  });
});
