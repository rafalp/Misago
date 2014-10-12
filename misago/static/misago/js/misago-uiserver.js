// Misago UI server
(function($) {

  // Class definition
  // ===============================

  var MisagoUIServer = function(frequency) {

    if (frequency == undefined) {
      frequency = 15000;
    }

    this.ui_observers = [];
    this.observer = function(name, callback) {
      if (callback == undefined) {
        this.ui_observers.push({callback: name});
      } else {
        this.ui_observers.push({name: name, callback: callback});
      }
    };

    this.query_server = function(poll) {
      if (poll === undefined) {
        poll = 0;
      }

      ui_observers = this.ui_observers
      $.get(uiserver_url, function(data) {
        $.each(ui_observers, function(i, observer) {
          if (observer.name == undefined) {
            observer.callback(data);
          } else if (typeof data[observer.name] !== "undefined") {
            observer.callback(data[observer.name]);
          }
        });

        $.misago_dom().changed();

        if (poll > 0) {
          window.setTimeout(function() {
            query_server(frequency);
          }, poll);
        }
      });
    };

    window.setTimeout(function() {
      query_server(frequency);
    }, 2000); // First request after 2 seconds

    // Return object
    return this;
  };

  // Plugin definition
  // ==========================

  $.misago_ui = function(frequency) {
    if ($._misago_ui == undefined) {
      $._misago_ui = MisagoUIServer(frequency);
    }
    return $._misago_ui;
  };

}(jQuery));
