// Register tooltips
$(function() {
  $('.tooltip-top').tooltip({placement: 'top', container: 'body'});
  $('.tooltip-bottom').tooltip({placement: 'bottom', container: 'body'});
  $('.tooltip-left').tooltip({placement: 'left', container: 'body'});
  $('.tooltip-right').tooltip({placement: 'right', container: 'body'});
});


// Tables
$(function() {
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
      return false;
    });
  });
});
