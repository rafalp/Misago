// Controller for reporting posts
$(function() {

  MisagoReportPost = function() {

    this._clear = function() {

      this.api_url = null;
      this.on_report = null;
      this.posted = false;

      this.$error = null;
      this.$form = null;

    }

    this._clear();

    var _this = this;

    this.open = function(api_url, on_report) {

      this._clear();

      if (!this.is_open()) {

        this.api_url = api_url;
        this.on_report = on_report;

        $.get(api_url, function(data) {

          if (data.is_reported) {
            Misago.Alerts.info(data.message);
          } else {
            Misago.Modal.show(data);

            _this.$form = Misago.Modal.$modal.find('form');

            _this.$error = Misago.Modal.$modal.find('.text-danger');
            _this.$error.hide();

            _this.$form.submit(function(e) {
              if (!_this.posted) {
                _this.posted = true;
                _this.submit();
              }
              e.preventDefault();
              return false;
            });

          }

        });

      }

    }

    this.submit = function() {

      $.post(this.api_url, this.$form.serialize(), function(data) {

        if (data.is_error) {

          _this.$error.text(data.message);
          _this.$error.slideDown();
          _this.posted = false;

        } else {

          Misago.Modal.close();
          Misago.Alerts.success(data.message);

          if (this.on_report) {
            this.on_report(data);
          }

        }

      });

    }

    this.is_open = function() {

      return Misago.Modal.is_visible();

    }

  }

  Misago.ReportPost = new MisagoReportPost();

});
