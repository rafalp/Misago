// Misago modal extension
(function($) {

  // Modal handler class definition
  // ===============================

  var MisagoModal = function() {

    this.$modal = $('#ajax-modal');
    this.$content = $('#ajax-modal .modal-content');

    this.is_visible = function() {
      return $('body').hasClass('modal-open');
    }

    this.show_modal = function(html) {
      if (this.is_visible()) {
        this.$content.fadeOut(200);
        this.$content.html(html);
        this.$content.fadeIn(200);
      } else {
        this.$content.html(html);
        this.$modal.modal({show: true});
      }
    }

    this.post = function(url, data) {
      var _this = this;
      $.post(url, data, function(data) {
        _this.show_modal(data);
        $.misago_dom().changed();
      });
    }

    // Return object
    return this;

  };

  // Plugin definition
  // ==========================

  $.misago_modal = function(options) {
    if ($._misago_modal == undefined) {
      $._misago_modal = MisagoModal();
    }
    return $._misago_modal;
  };

}(jQuery));
