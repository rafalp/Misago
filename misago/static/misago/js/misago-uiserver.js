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
      this.ui_observers.push({name: name, callback: callback});
      this.query_server();
    };

    this.query_server = function(poll) {
      if (poll === undefined) {
        poll = 0;
      }

      ui_observers = this.ui_observers
      $.get(uiserver_url, function(data) {
        $.each(ui_observers, function(i, observer) {
          if (typeof data[observer.name] !== "undefined") {
            observer.callback(data[observer.name]);
          }
        });

        if (poll > 0) {
          window.setTimeout(function() {
            query_server(frequency);
          }, poll);
        }
      });
    };

    window.setTimeout(function() {
      query_server(frequency);
    }, frequency);

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
