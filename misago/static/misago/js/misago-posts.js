// Controller for posts lists
$(function() {

  // Post controller

  MisagoPost = function($element) {

    this.$e = $element;
    this.$alerts = this.$e.find('.post-alerts');
    this.$content = this.$e.find('article.post-body');
    this.id = this.$e.data('id');

    var _this = this;

    this.focus = function() {
      this.$e.addClass('focus');
    }

    this.remove_focus = function() {
      this.$e.removeClass('focus');
    }

    this.change_post = function(new_content) {
      this.$content.fadeTo('fast', 0.1, function() {
        _this.$content.html(new_content);
        Misago.Onebox.activate(_this.$content);
        Misago.DOM.changed();

        _this.$content.fadeTo('fast', 1);
      });
    }

    this.$e.find('.btn-edit').click(function() {

      if (!Misago.Posting.is_open() || Misago.Posting.cancel()) {
        Misago.Posting.load({
          api_url: _this.$e.data('edit-url'),
          on_load: function() {
            _this.focus();
          },
          on_cancel: function() {
            _this.remove_focus();
          },
          on_post: function(data) {
            Misago.Alerts.success(data.message);
            _this.change_post(data.parsed);

            if (Misago.Posting.$form.find('.thread-title').length == 1) {
              var old_title = $.trim($('#thread-title').html());
              $('#thread-title').html(data.title_escaped);
              document.title = document.title.replace(old_title, data.title_escaped)
            }

            Misago.Posting.cancel();
            Misago.Scroll.scrollTo(_this.$e);
            return false;
          }
        });
      }

    });

    this.$report = this.$e.find('.btn-report');
    this.$report.click(function() {

      if (!Misago.ReportPost.is_open()) {
        Misago.ReportPost.open(_this, _this.$e.data('report-url'), function(data) {
          _this.$alerts.html(data.alerts);
          _this.$alerts.fadeIn();
          _this.$report.attr('disabled', 'disabled');
          _this.$report.find('.btn-label').text(data.label);
        });
      }

    });

    this.quote = function() {

      $.get(_this.$e.data('quote-url'), function(data) {
        Misago.Posting.append(data.quote);
      });

    }

    this.$e.find('.btn-reply').click(function() {

      if (!Misago.Posting.is_open()) {
        Misago.reply_thread(function() {
          _this.quote();
        });
      } else {
        _this.quote();
      }

    });

    this.$e.find('form').submit(function() {

      var prompt = $(this).data('prompt');
      if (prompt) {
        var decision = confirm(prompt);
        return decision;
      } else {
        return true;
      }

    });

  }

  // Posts controller

  MisagoPosts = function() {

    this.posts = {};

    var _this = this;

    // discover posts data

    this.discover_posts = function() {
      $('.thread-post').each(function() {
        var id = $(this).data('id');
        _this.posts[id] = new MisagoPost($(this));
      });
    }
    this.discover_posts();

  }

  Misago.Posts = new MisagoPosts();

  // Mass actions controller

  function PostsMassActions() {

    var $form = $('#posts-actions');
    var $btn = $form.find('.mass-controller');

    var btn_label = $btn.html();

    // handle moderation form
    var select_items_message = $('#posts-actions').data('select-items-message');

    function update_btn_label() {
      var selected_items = $('.post-check.active').length;

      if (selected_items > 0) {
        $btn.html(btn_label + "(" + selected_items + ")");
      } else {
        $btn.html(btn_label);
      }
    }

    $('.post-check').each(function() {

      var $check = $(this);

      var $checkbox = $check.find('input');
      if ($checkbox.prop("checked")) {
        $check.addClass('active');
      }

      $check.on("click", function() {
        $check.toggleClass('active');
        if ($check.hasClass('active')) {
          $checkbox.prop("checked", true);
        } else {
          $checkbox.prop("checked", false);
        }

        update_btn_label();
        return false;
      });

    });
    update_btn_label();

    $form.find('li button').click(function() {
      if ($(this).data('confirmation')) {
        var confirmation = confirm($(this).data('confirmation'));
        return confirmation;
      } else {
        return true;
      }
    });

    $form.submit(function() {
      if ($('.post-check.active').length == 0) {
        alert(select_items_message);
        return false;
      } else {
        return true;
      }
    });

  }
  PostsMassActions();

});
