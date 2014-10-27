// Controller for posts lists
$(function() {

  MisagoPost = function($element) {

    this.$e = $element;
    this.$content = this.$e.find('.post-body');
    this.id = this.$e.data('id');

    var _this = this;

    this.highlight = function() {
      $element.addClass('highlighted');
    }

    this.remove_highlight = function() {
      $element.removeClass('highlighted');
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
            _this.highlight();
          },
          on_cancel: function() {
            _this.remove_highlight();
          },
          on_post: function(data) {
            Misago.Alerts.success(data.message);
            _this.change_post(data.parsed);
            Misago.Posting.cancel();
            return false;
          }
        });
      }

    });

  }

  MisagoPosts = function() {

    this.posts = {};

    var _this = this;

    this.discover_posts = function() {
      $('.thread-post').each(function() {
        var id = $(this).data('id');
        _this.posts[id] = new MisagoPost($(this));
      });
    }
    this.discover_posts();

  }

  Misago.Posts = new MisagoPosts();

});
