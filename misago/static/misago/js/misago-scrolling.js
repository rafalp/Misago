// Scrolling behaviour fixes
$(function() {

  // we are meddling in window.location, which means we need js fix scrolls to fragments
  if(window.location.hash) {
      $(document.body).animate({
        'scrollTop': $(window.location.hash).offset().top
      }, 500);
  }

  // scrolling enhancement for overflow: scroll elements
  function handle_scroll($element, e) {
    var scroll = $element.scrollTop();

    if (scroll == 0 && e.deltaY > 0 ) {
      // block scroll of whole page when user ends scrolling item up
      e.preventDefault();
    }

    if ($element[0].scrollHeight - $element.innerHeight() - scroll == 0 && e.deltaY < 0 ) {
      // block scroll of whole page when user ends scrolling item down
      e.preventDefault();
    }
  }

  function add_scroll_handlers() {
    $('.scrollable').each(function() {
      if ($(this).data('misago-scroolable') == undefined) {
        $(this).data('misago-scroolable', true);
        $(this).on('mousewheel', function(e) {
          handle_scroll($(this), e);
        });
      }
    });
  }

  Misago.DOM.on_change(add_scroll_handlers);

});
