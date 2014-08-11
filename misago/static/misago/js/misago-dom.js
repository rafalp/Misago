// Misago DOM upades helper
(function($) {

  // Events sender
  // ===============================

  var MisagoDOM = function() {

    this.dom_listeners = [];
    this.change = function(callback) {
      this.dom_listeners.push(callback);
      callback();
    };

    this.changed = function() {
      $.each(this.dom_listeners, function(i, callback) {
        callback();
      });
    };

    // Return object
    return this;
  };

  // Plugin definition
  // ==========================

  $.misago_dom = function() {
    if ($._misago_dom == undefined) {
      $._misago_dom = MisagoDOM();
    }
    return $._misago_dom;
  };

}(jQuery));
