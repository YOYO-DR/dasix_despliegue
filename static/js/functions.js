function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    }
    else{
        html = '<p>'+obj+'</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}

function submit_with_ajax(url,title, content, parametros,callback) {
    $.confirm({
      theme: "material", 
      title: title, 
      icon: "fa fa-info", 
      content: content, 
      columnClass: "medium", 
      typeAnimated: true,
      cancelButtonClass: "btn-primary",
      draggable: true, 
      dragWindowBorder: false,
      buttons: {
        info: {
          text: "Si", 
          btnClass: "btn-green",
          action: function () {
            $.ajax({
              url: url, 
              type: "POST",
              data: parametros, 
              dataType: "json",
              processData: false,
              contentType: false
            })
              .done(function (data) {
                if (!data.hasOwnProperty("error")) {
                  callback(); 
                  return false;
                }
                message_error(data.error);
              })
              .fail(function (jqXHR, textStatus, errorThrown) {
                alert(`${textStatus} : ${errorThrown}`);
              })
              .always(function () {
              });
          },
        },
        danger: {
          text: "No",
          btnClass: "btn-red",
          action: function () {},
        },
      },
    });
  };

  function alert_action(title, content, callback) {
    $.confirm({
      theme: "material", 
      title: title, 
      icon: "fa fa-info", 
      content: content, 
      columnClass: "medium", 
      typeAnimated: true,
      cancelButtonClass: "btn-primary",
      draggable: true, 
      dragWindowBorder: false,
      buttons: {
        info: {
          text: "Si", 
          btnClass: "btn-green",
          action: function () {
            callback();
          }
        },
        danger: {
          text: "No",
          btnClass: "btn-red",
          action: function () {},
        },
      },
    });
};

// Configurar el token CSRF globalmente para todas las solicitudes AJAX
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    }
});