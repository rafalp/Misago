$(function() {
  function MisagoNotifications() {

    _this = this;

    this.ajax_cache = null;

    this.$container = $('.user-notifications-nav');
    this.$link = this.$container.find('.dropdown-toggle');

    this.$display = this.$container.find('.display');
    this.$loader = this.$container.find('.loader');

    this.on_data = function(data) {
      Tinycon.setBubble(data.count);
      if (_this.ajax_cache != null && data.count != _this.ajax_cache.count) {
        _this.ajax_cache = null;
        if (_this.$container.hasClass('open')) {
          _this.$container.find('.btn-refresh').fadeIn();
          if (data.count > 0) {
            _this.$container.find('.btn-read-all').fadeIn();
          } else {
            _this.$container.find('.btn-read-all').fadeOut();
          }
        }
      }
    }

    if (is_authenticated) {
      Misago.Server.on_data("notifications", this.on_data);
    }

    this.handle_list_response = function(data) {
      _this.ajax_cache = data;
      _this.$loader.hide();
      _this.$display.html(data.html);
      _this.$display.show();
      Misago.DOM.changed();
    }

    this.fetch_list = function() {
      $.get(_this.$link.attr('href'), function(data) {
        _this.handle_list_response(data)
      });
    }

    this.$container.on('click', '.btn-refresh', function() {
      _this.$display.hide();
      _this.$loader.show();
      _this.fetch_list();
    });

    this.$container.on('show.bs.dropdown', function () {
      if (_this.ajax_cache == null) {
        _this.fetch_list();
      }
    });

    this.$container.on('hide.bs.dropdown', function() {
      _this.$container.find('.btn-refresh').hide();
    });

    this.$container.on('submit', '.read-all-notifications', function() {
      _this.$display.hide();
      _this.$loader.show();
      $.post($link.attr('href'), $(this).serialize(), function(data) {
        _this.handle_list_response(data);
        Misago.Server.update()
      });
      return false;
    });

  }

  Misago.Notifications = MisagoNotifications();

});
