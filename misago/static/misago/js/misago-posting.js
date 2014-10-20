// Controller for posting actions
$(function() {
  MisagoPreview = function(_controller, options) {

    this.$form = options.form;
    this.$area = $(options.selector);

    this.$markup = this.$area.find('.misago-markup');
    this.$message = this.$area.find('.empty-message');

    if (this.$markup.text() == '') {
      this.$markup.hide();
    }

    this.api_url = options.api_url;
    this.active = true;
    this.previewed_data = this.$form.serialize() + '&preview=1';


    this.frequency = 1500;

    this.height = this.$markup.height();

    var _this = this;

    this.last_key_press = (new Date().getTime() / 1000);
    this.$form.find('.misago-editor textarea').keyup(function() {
      _this.last_key_press = (new Date().getTime() / 1000);
    })

    this.update = function() {
      var form_data = _this.$form.serialize() + '&preview=1';
      var last_key = (new Date().getTime() / 1000) - _this.last_key_press;

      if (_this.previewed_data != form_data && last_key > 2) {
        $.post(_this.api_url, form_data, function(data) {
          var scroll = $(document).height() - $(document).scrollTop();

          if (data.preview) {
            if (_this.$message.is(":visible")) {
              _this.$message.fadeOut(function() {
                _this.$markup.html(data.preview);
                _this.$markup.fadeIn();
              });
            } else {
              _this.$markup.html(data.preview);
            }

            if (_this.$markup.height() > _this.height) {
              $(document).scrollTop($(document).height() - scroll);
            }
          } else {
            _this.$markup.fadeOut(function() {
              _this.$markup.html("");
              _this.$message.fadeIn();
            });
          }

          _controller.update_affix_end();
          _controller.update_affix();
          Misago.DOM.changed();

          _this.previewed_data = form_data;

          // set timeout
          if (_this.active) {
            window.setTimeout(function() {
              _this.update();
            }, _this.frequency);
          }

        });
      } else if (_this.active) {
        window.setTimeout(function() {
          _this.update();
        }, _this.frequency);
      }
    }

    this.stop = function() {
      this.active = false;
    }

  }

  MisagoPosting = function() {

    this.$spacer = null;
    this.$container = null;
    this.$form = null;

    this.$preview = null;

    this.affix_end = 0;

    var _this = this;

    this.init = function(options) {

      this.$form = $('#posting-form');
      this.$container = this.$form.parent();
      this.$spacer = this.$container.parent();

      if (options.preview !== undefined) {
        this.$preview = new MisagoPreview(this, {selector: options.preview, form: this.$form, api_url: options.api_url});
        this.$preview.update();
      }

      this.container_height = this.$container.innerHeight();
      this.$spacer.height(this.container_height);

      this.heights_diff = this.$container.outerHeight() - this.$spacer.innerHeight();

      this.update_affix_end();
      this.update_affix();

      $(document).scroll(function() {
        _this.update_affix()
      });

    }

    this.update_affix_end = function() {
      this.spacer_end = this.$spacer.offset().top + this.$spacer.height();
    }

    this.update_affix = function() {
      if (this.spacer_end - $(document).scrollTop() > $(window).height()) {
        this.$container.addClass('fixed');
      } else {
        this.$container.removeClass('fixed');
      }
    }

  }

  Misago.Posting = new MisagoPosting();
});
