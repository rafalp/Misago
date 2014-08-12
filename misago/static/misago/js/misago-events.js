// Misago events extension
(function($) {

  // Events handler class definition
  // ===============================

  var MisagoEvents = function(frequency) {

    if (frequency == undefined) {
      this.frequency = 15000;
    } else {
      this.frequency = frequency;
    }

    this.listeners = [];
    this.listener = function(url, callback) {
      this.listeners.push({url: url, callback: callback});
      this.poll(true);
    };

    this.poll = function(mute_timeout) {
      var poll = this.poll;
      var frequency = this.frequency;

      var ajax_calls = [];
      $.each(this.listeners, function(i, obj) {
        ajax_calls.push($.get(obj.url));
      });

      var listeners = this.listeners;
      $.when.apply($, ajax_calls).then(function () {
          var _args = arguments;
          var events_count = 0;

          if (listeners.length == 1) {
            var data = _args[0];
            events_count = data.count;
            listeners[0].callback(data);
          } else {
            $.each(listeners, function(i, obj) {
              var data = _args[i][0];
              events_count += data.count;
              obj.callback(data);
            });
          }
          Tinycon.setBubble(events_count);
          if (mute_timeout === undefined || mute_timeout == false){
            window.setTimeout(poll, frequency);
          }
      });
    };
    window.setTimeout(this.poll, this.frequency);

    // Return object
    return this;
  };

  // Plugin definition
  // ==========================

  $.misago_events = function(frequency) {
    if ($._misago_events == undefined) {
      $._misago_events = MisagoEvents(frequency);
    }
    return $._misago_events;
  };

}(jQuery));
