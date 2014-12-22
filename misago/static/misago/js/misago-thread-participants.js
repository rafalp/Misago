MisagoThreadParticipants = function() {

    var _this = this;

    this.clear = function() {

      this.$container = null;
      this.max_participants = 1;

    }

    this.init = function($container) {

      this.$container = $container;

      this.$users = $container.find('ul');
      this.$message = $container.find('.message');
      this.$form = $container.find('.invite-form');

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

}


$(function() {
  Misago.ParticipantsEditor = new MisagoThreadParticipants();
});
