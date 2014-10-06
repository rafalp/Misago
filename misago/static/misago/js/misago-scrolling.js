$('.scrollable').on('mousewheel', function(e) {
  var scroll = $(this).scrollTop();

  if (scroll == 0 && e.deltaY > 0 ) {
    // block scroll of whole page when user ends scrolling item up
    e.preventDefault();
  }

  if ($(this)[0].scrollHeight - $(this).innerHeight() - scroll == 0 && e.deltaY < 0 ) {
    // block scroll of whole page when user ends scrolling item down
    e.preventDefault();
  }
});
