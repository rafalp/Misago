$(function() {

  // don't close dropdown when click happens inside it
  $('.dropdown').on("hide.bs.dropdown", function(e) {
    if ($.contains(this, event.target)) {
      e.preventDefault();
    }
  });

});
