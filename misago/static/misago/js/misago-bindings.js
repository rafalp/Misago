// Extra data bindings
$(function() {
  // hide all pop-ins
  $('[data-misago-pop-in]').hide();

  // update bindings on new data from server
  Misago.Server.on_data(function(data) {
    // Update and fade in/out badges
    $('[data-misago-badge]').each(function() {
      var new_value = Misago.getattr(data, $(this).data('misago-badge'));
      if (new_value != undefined) {
        $(this).text(new_value);
        if (new_value > 0) {
          $(this).addClass("in");
        } else {
          $(this).removeClass("in");
        }
      }
    });

    // update text
    $('[data-misago-text]').each(function() {
      var new_value = Misago.getattr(data, $(this).data('misago-text'));
      if (new_value != undefined) {
        $(this).text(new_value);
      }
    });

    // fade in/out depending on value
    $('[data-misago-fade-in]').each(function() {
      var new_value = Misago.getattr(data, $(this).data('misago-fade-in'));
      if (new_value != undefined) {
        if (new_value > 0) {
          $(this).addClass("in");
        } else {
          $(this).removeClass("in");
        }
      }
    });

    // pop in/out depending on value
    $('[data-misago-pop-in]').each(function() {
      var new_value = Misago.getattr(data, $(this).data('misago-pop-in'));
      if (new_value != undefined) {
        if (new_value > 0) {
          $(this).slideIn();
        } else {
          $(this).slideOut();
        }
      }
    });
  });
});
