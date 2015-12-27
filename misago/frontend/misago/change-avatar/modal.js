(function (Misago) {
  'use strict';

  var ViewModel = function(user, _) {
    var self = this;

    this.isBusy = false;

    this.user = user;
    this.options = null;
    this.component = _.component('change-avatar:loading', self);

    this.api = _.ajax.buildApiUrl(['users', user.id, 'avatar']);

    // Load user avatar options
    _.ajax.get(this.api).then(function(options) {
      m.startComputation();

      self.options = options;
      self.component = _.component('change-avatar:start', self);

      m.endComputation();
    }, function(rejection) {
      if (rejection.status === 403) {
        m.startComputation();

        self.component = _.component('change-avatar:denied', rejection);

        m.endComputation();
      } else {
        _.modal();
        _.ajax.error(rejection);
      }
    });

    // Avatar actions
    var avatarRpc = function(avatarType) {
      if (self.isBusy) {
        return;
      }

      self.isBusy = true;

      _.ajax.post(self.api, {avatar: avatarType}).then(function(response) {
        m.startComputation();

        _.alert.success(response.detail);
        self.options = response.options;
        self.user.avatar_hash = response.avatar_hash;

        self.isBusy = false;

        m.endComputation();
      }, function(rejection) {
        _.modal();
        _.ajax.error(rejection);
      })
    };

    this.downloadGravatar = function() {
      avatarRpc('gravatar');
    };

    this.generateAvatar = function() {
      avatarRpc('generated');
    };
  };

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  var modal = {
    class: '.modal-dialog.modal-form.modal-change-avatar',

    controller: function(user, _) {
      return {
        vm: new ViewModel(user, _)
      };
    },
    view: function(ctrl, user, _) {
      return m(this.class + '[role="document"]', {config: persistent},
        m('.modal-content', [
          _.component('modal:header', gettext("Change avatar")),
          ctrl.vm.component
        ])
      );
    }
  };

  Misago.addService('modal:change-avatar', function(_) {
    _.modal('change-avatar', modal);
  },
  {
    after: 'modals'
  });
}(Misago.prototype));
