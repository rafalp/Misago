// Mass-action for threads list
function threadsMassActions() {
  var $form = $('#threads-actions');
  var $master = $('.master-checkbox');
  var $threads = $('.table-panel .list-group-item');

  var select_items_message = $form.data('select-items-message');

  $form.find('li button').click(function() {
    if ($(this).data('confirmation')) {
      var confirmation = confirm($(this).data('confirmation'));
      return confirmation;
    } else {
      return true;
    }
  });

  $master.click(function() {
    if ($threads.filter('.active').length == $threads.length) {
      $threads.removeClass('active');
      $threads.find('.thread-check').removeClass('active');
      $threads.find('.thread-check input').prop("checked", false);
      $master.removeClass('active');
    } else {
      $threads.addClass('active');
      $threads.find('.thread-check').addClass('active');
      $threads.find('.thread-check input').prop("checked", true);
      $master.addClass('active');
    }
  });

  $threads.each(function() {
    var $row = $(this);

    var $checkbox = $(this).find('.thread-check input');
    if ($checkbox.prop("checked")) {
      $row.addClass('active');
      $(this).find('.thread-check').addClass('active');
    }

    $row.find('.thread-check').on("click", function() {
      var $row = $(this).parents('.list-group-item');
      var $checkbox = $(this).find('input');

      $(this).toggleClass('active');
      if ($(this).hasClass('active')) {
        $checkbox.prop("checked", true);
        $row.addClass('active');
        if ($threads.filter('.active').length == $threads.length) {
          $master.addClass('active');
        }
      } else {
        $checkbox.prop("checked", false);
        $row.removeClass('active');
        $master.removeClass('active');
      }
      return false;
    });
  });

  $form.submit(function() {
    if ($threads.filter('.active').length == 0) {
      alert(select_items_message);
      return false;
    } else {
      return true;
    }
  });
}
