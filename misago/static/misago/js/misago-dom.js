// Event controller for DOM changes
var MisagoDOM = function() {

  this.dom_listeners = [];
  this.on_change = function(callback) {
    this.dom_listeners.push(callback);
    callback();
  };

  this.changed = function() {
    $.each(this.dom_listeners, function(i, callback) {
      callback();
    });
  };

};

Misago.DOM = new MisagoDOM();
