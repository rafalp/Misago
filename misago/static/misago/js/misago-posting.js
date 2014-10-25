// Controller for posting actions
$(function() {

  MisagoPreview = function(_controller, options) {

    this.$form = options.form;
    this.$area = options.$area;
    this.$frame = this.$area.find('.frame');

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

    this.$frame.height(this.$form.find('.misago-editor').innerHeight() - this.$area.find('.preview-footer').outerHeight());

    this.update = function() {
      var form_data = _this.$form.serialize() + '&preview=1';
      var last_key = (new Date().getTime() / 1000) - _this.last_key_press;

      if (_this.previewed_data != form_data && last_key > 2) {
        $.post(_this.api_url, form_data, function(data) {
          var scroll = _this.$markup.height() - _this.$frame.scrollTop();

          if (data.preview) {
            if (_this.$message.is(":visible")) {
              _this.$message.fadeOut(function() {
                _this.$markup.html(data.preview);
                Misago.Onebox.activate(_this.$markup);
                _this.$markup.fadeIn();
              });
            } else {
              _this.$markup.html(data.preview);
              Misago.Onebox.activate(_this.$markup);
            }

            if (_this.$markup.height() > _this.height) {
              _this.$frame.scrollTop(_this.$markup.height() - scroll);
            }
          } else {
            _this.$markup.fadeOut(function() {
              _this.$markup.html("");
              _this.$message.fadeIn();
              _this.$frame.scrollTop(0);
            });
          }

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

    this._clear = function() {

      this.$spacer = null;
      this.$container = null;
      this.$form = null;

      this.$ajax_loader = null;
      this.$ajax_complete = null;

      this.$preview = null;

      this.submitted = false;
      this.posted = false;

      this.affix_end = 0;

      this.on_cancel = null;

    }

    this._clear();

    var _this = this;

    this.init = function(options) {

      if (this.$form !== null) {
        return false;
      }

      this.$form = $('#posting-form');
      this.$container = this.$form.parent();
      this.$spacer = this.$container.parent();

      if (options.on_cancel !== undefined) {
        this.on_cancel = options.on_cancel
      } else {
        this.on_cancel = null;
      }

      this.$ajax_loader = this.$container.find('.ajax-loader');
      this.$ajax_complete = this.$container.find('.ajax-complete');

      this.$preview = new MisagoPreview(this, {$area: this.$form.find('.editor-preview'), form: this.$form, api_url: options.api_url});
      this.$preview.update();

      // target height is 26 px too big
      this.$spacer.height(this.$container.outerHeight() - ($(document).height() - this.$spacer.offset().top));
      this.$container.addClass('fixed');

      this.$container.find('button[name="submit"]').click(function() {
        if (!_this.submitted && !_this.posted) {
          _this.submitted = true; // lock submit process until after response
          _this.$ajax_loader.addClass('in');

          var form_data = _this.$form.serialize() + '&submit=1';
          $.post(options.api_url, form_data, function(data) {
            _this.$ajax_loader.removeClass('in');
            if (data.post_url !== undefined) {
              _this.posted = true;
              _this.$ajax_loader.hide();
              _this.$ajax_complete.addClass('in')

              if (data.post_url.indexOf(window.location.pathname) != -1) {
                window.location.href = data.post_url;
                window.location.reload(true)
              } else {
                window.location.href = data.post_url;
              }
            } else if (data.errors !== undefined) {
              Misago.Alerts.error(data.errors[0]);
            } else if (data.interrupt !== undefined) {
              Misago.Alerts.info(data.interrupt);
            } else {
              Misago.Alerts.error();
            }

            _this.submitted = false;
          });
        }

        return false;
      })

      this.$container.find('button[name="cancel"]').click(function() {

        if (_this.has_content()) {
          var decision = confirm(lang_dismiss_editor);
          if (decision) {
            _this.cancel();
          }
        } else {
          _this.cancel();
        }

        return false;
      });

      return true;

    }

    this.load = function(options) {

      if (this.$form !== null) {
        return false;
      }

      $.get(options.api_url, function(data) {
        $('#reply-form-placeholder').html(data);
        Misago.DOM.changed();
        _this.init(options);
        Misago.DOM.changed();

        if (options.on_load !== undefined) {
          options.on_load();
        }
      });

    }

    this.cancel = function() {

      if (this.$form !== null) {

        if (this.$preview !== null) {
          this.$preview.stop();
        }

        this.$spacer.fadeOut(function() {
          $(this).remove();
          $('.main-footer').show();
        });

        if (this.on_cancel !== undefined) {
          this.on_cancel();
        }

        this._clear();
      }

    }

    this.has_content = function() {

      if (_this.$form !== null) {
        var length = $.trim(_this.$form.find('input[name="title"]').val()).length;
        length += $.trim(_this.$form.find('textarea').val()).length;
        return length > 0;
      } else {
        return false;
      }

    }

  }

  Misago.Posting = new MisagoPosting();

  $(window).on("beforeunload", function() {
    if (Misago.Posting.has_content() && !Misago.Posting.posted) {
      return lang_dismiss_editor;
    }
  })
});
