MisagoThreadParticipants = function() {

    var _this = this;

    this.clear = function() {

      this.$container = null;
      this.max_participants = 1;
      this.deleted_ids = [];

    }

    this.init = function($container) {

      this.$container = $container;

      this.$users = $container.find('ul');
      this.$message = $container.find('.message');
      this.$error = $container.find('.text-danger');
      this.$form = $container.find('form');

      this.max_participants = parseInt($container.data('max-participants'));

      this.$message.hide();
      this.$form.hide();

      if (this.$users.find('li').length < this.max_participants) {
        this.$form.show();
      } else {
        this.$message.show();
      }

      // suppress default submission handling

      this.$container.find('form').submit(function(e) {

        e.preventDefault();
        return false;

      })

      this.participants = new Misago.Participants(this.$form.find('.thread-participants-input'));

      // buttons

      this.$container.find('.btn-add-participants').click(function() {

        _this.add($(this).data('add-url'));

      })

      this.$container.find('.btn-remove-participant').click(function() {

        var $participant = $(this).parents('li.participant');
        _this.remove($participant, $(this).data('remove-url'));

      })

    }

    this.update_list = function(new_html) {

      this.$users.html(new_html);
      this.$container.find('.btn-remove-participant').click(function() {

        var $participant = $(this).parents('li.participant');
        _this.remove($participant, $(this).data('remove-url'));

      })

    }

    this.update_form_visibility = function() {

      if (this.$users.find('li').length < this.max_participants) {
        this.$message.hide();
        this.$form.fadeIn();
      } else {
        this.$form.hide();
        this.$message.fadeIn();
      }

    }

    this.open = function(options) {

      this.clear();

      Misago.Modal.get(options.api_url, function(data) {

        _this.init($('.modal-edit-participants'));

      });

    }

    this.add = function(api_url) {

      $.post(api_url, this.$form.serialize(), function(data) {

        if (data.is_error) {
          _this.$error.text(data.message);
          _this.$error.addClass('in');
        } else {
          _this.$error.removeClass('in');
          $('.participants-message').text(data.message);
          _this.update_list(data.list_html);
          _this.participants.clear();
        }

        _this.update_form_visibility();

      });

    }

    this.remove = function($participant, api_url) {

      var participant_id = $participant.data('participant-id');

      if (this.deleted_ids.indexOf(participant_id) == -1) {

        this.deleted_ids.push(participant_id);

        $participant.slideUp();

        $.post(api_url, this.$form.serialize(), function(data) {

          $participant.remove();
          if (data.is_error) {
            alert(data.message);
          } else {
            $('.participants-message').text(data.message);
          }

        }).fail(function() {

          var deleted_id_pos = _this.deleted_ids.indexOf(participant_id);
          _this.deleted_ids.splice(deleted_id_pos, 1);
          $participant.slideDown();

        });

      }

    }

}


$(function() {
  Misago.ParticipantsEditor = new MisagoThreadParticipants();
});
