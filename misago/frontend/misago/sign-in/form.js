(function (Misago) {
  'use strict';

  var SignIn = function(_) {
    var self = this;

    this.showActivation = false;

    this.username = m.prop('');
    this.password = m.prop('');

    this.validation = {
      'username': [],
      'password': []
    };

    this.clean = function() {
      if (!_.validate(this)) {
        _.alert.error(gettext("Fill out both fields."));
        return false;
      } else {
        return true;
      }
    };

    this.submit = function() {
      _.api.endpoint('auth').post({
        username: self.username(),
        password: self.password()
      }).then(function() {
        self.success();
      }, function(error) {
        self.error(error);
      });
    };

    this.success = function() {
      _.modal();

      var $form = $('#hidden-login-form');

      // refresh CSRF token because api call to /auth/ changed it
      _.ajax.refreshCsrfToken();

      // fill out form with user credentials and submit it, this will tell
      // misago to redirect user back to right page, and will trigger browser's
      // key ring feature
      $form.find('input[type="hidden"]').val(_.ajax.csrfToken);
      $form.find('input[name="redirect_to"]').val(m.route());
      $form.find('input[name="username"]').val(this.username());
      $form.find('input[name="password"]').val(this.password());
      $form.submit();
    };

    this.error = function(rejection) {
      if (rejection.status === 400) {
        if (rejection.code === 'inactive_admin') {
          _.alert.info(rejection.detail);
        } else if (rejection.code === 'inactive_user') {
          _.alert.info(rejection.detail);
          self.showActivation = true;
        } else if (rejection.code === 'banned') {
          _.showBannedPage(rejection.detail);
          _.modal();
        } else {
          _.alert.error(rejection.detail);
        }
      } else {
        _.api.alert(rejection);
      }
    };
  };

  Misago.addService('form:sign-in', function(_) {
    _.form('sign-in', SignIn);
  },
  {
    after: 'forms'
  });
} (Misago.prototype));
