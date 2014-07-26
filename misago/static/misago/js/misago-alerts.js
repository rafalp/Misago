// Misago alerts extension
(function($) {

  // Alerts handler class definition
  // ===============================

  var MisagoAlerts = function(options) {

    this.options = $.extend({
      alerts_container: ".misago-alerts",
      generic_error: "Unspecified error occured",
      error_template: "",
      info_template: "",
      success_template: ""
    }, options);

    // Get DOM elements
    this.$alerts = $(this.options.alerts_container);
    this.$alerts_list = this.$alerts.find('.alerts-list');

    // Store and freeze alerts list height for affix
    this.$height = this.$alerts.height();
    this.$alerts.height(this.$height);

    // Affix alerts
    this.$alerts_list.affix({
      offset: {
        top: this.$alerts.offset().top
      }
    });

    // Slide up alert
    function bindCloseEvents(controller) {
      controller.$alerts_list.on('click', '.alert-div .close', function() {
        var $alert = $(this).parent().parent();
        controller.$height -= $alert.height();
        controller.$alerts.animate({height: controller.$height}, {queue: false});
        $alert.slideUp();
      });
    }
    bindCloseEvents(this);

    // Alerts functions
    this.add_alert = function(template, message) {
      var $alert = $(template.replace('%message%', message));
      this.$alerts_list.append($alert);

      this.$height += $alert.height();
      $alert.hide();
      this.$alerts.animate({height: this.$height}, {queue: false});
      $alert.slideDown();
    }

    this.error = function(message) {
      this.add_alert(self.options.error_template, message);
    }

    this.info = function(message) {
      this.add_alert(self.options.info_template, message);
    }

    this.success = function(message) {
      this.add_alert(self.options.success_template, message);
    }

    // Return object
    return this;

  };

  // Plugin definition
  // ==========================

  $.misago_alerts = function(options) {
    if ($._misago_alerts == undefined) {
      $._misago_alerts = MisagoAlerts(options)
    }
    return $._misago_alerts;
  };

}(jQuery));
