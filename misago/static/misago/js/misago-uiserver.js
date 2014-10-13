// Misago UI server
var MisagoUIServer = function(frequency) {

  if (frequency == undefined) {
    frequency = 15000;
  }

  this.frequency = frequency;
  var _this = this;

  this.listeners = [];
  this.on_data = function(name, callback) {
    if (callback == undefined) {
      this.listeners.push({callback: name});
    } else {
      this.listeners.push({name: name, callback: callback});
    }
  };

  this.update = function() {
    $.get(uiserver_url, function(data) {

      $.each(_this.listeners, function(i, listener) {
        if (listener.name == undefined) {
          listener.callback(data);
        } else if (typeof data[listener.name] !== "undefined") {
          listener.callback(data[listener.name]);
        }
      });

      Misago.DOM.changed();

      window.setTimeout(function() {
        _this.update();
      }, _this.frequency);

    });
  };

}


// Create server and start it 2 seconds after dom ready
Misago.Server = new MisagoUIServer();
$(function() {
  window.setTimeout(function() {
    Misago.Server.update();
  }, 2000);
});
