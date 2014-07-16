// Mass-action tables
function tableMassActions(label_none, label_selected) {
  var $controller = $('.mass-controller');
  var $form = $controller.parents('form');

  $form.find('.dropdown-menu button').click(function() {
    if ($(this).data('confirmation')) {
      var confirmation = confirm($(this).data('confirmation'));
      return confirmation;
    } else {
      return true;
    }
  });

  function enableController(selected_no) {
      $controller.removeClass('btn-default');
      $controller.addClass('btn-primary');

      var fin_label = label_selected.replace(0, selected_no)
      $controller.html('<span class="fa fa-gears"></span> ' + fin_label);
      $controller.prop("disabled", false);
  }

  function disableController() {
      $controller.removeClass('btn-primary');
      $controller.addClass('btn-default');
      $controller.html('<span class="fa fa-exclamation-circle"></span> ' + label_none);
      $controller.prop("disabled", true);
  }

  $('.table tr').each(function() {
    var $row = $(this);
    var $checkbox = $row.find('input[type=checkbox]');
    var $label = $checkbox.parent();

    $label.addClass('ninja-label');
    $label.parent().append('<a href="#"><span class="fa fa-check"></span></a>');
    var $check = $label.parent().find('a');

    if ($checkbox.prop("checked")) {
      $check.toggleClass('active');
      $row.addClass('active');
    }

    $check.click(function() {
      $(this).toggleClass('active');
      if ($(this).hasClass('active')) {
        $(this).parent().find('input').prop("checked", true);
        $row.addClass('active');
      } else {
        $(this).parent().find('input').prop("checked", false);
        $row.removeClass('active');
      }

      var selected_no = $('.table tr.active').length
      if (selected_no > 0) {
        enableController(selected_no);
      } else {
        disableController();
      }
      return false;
    });

    var selected_no = $('.table tr.active').length
    if (selected_no > 0) {
      enableController(selected_no);
    } else {
      $controller.html('<span class="fa fa-exclamation-circle"></span> ' + label_none);
      $controller.prop("disabled", true);
    }
  });
}
