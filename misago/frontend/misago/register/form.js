(function (Misago) {
  'use strict';

  var Register = function(_) {
    var self = this;

    this.showActivation = false;

    this.username = m.prop('');
    this.email = m.prop('');
    this.password = m.prop('');

    this.captcha = _.captcha.value;

    this.errors = null;

    this.validation = {
      'username': [
        Misago.validators.usernameContent(),
        Misago.validators.usernameMinLength(_.settings),
        Misago.validators.usernameMaxLength(_.settings)
      ],
      'email': [
        Misago.validators.email()
      ],
      'password': [
        Misago.validators.passwordMinLength(_.settings)
      ],
      'captcha': _.captcha.validator()
    };

    this.clean = function() {
      if (this.errors === null) {
        _.validate(this);
      }

      _.captcha.clean(this);

      if (this.hasErrors()) {
        _.alert.error(gettext("Form contains errors."));
        return false;
      } else {
        return true;
      }
    };

    this.submit = function() {
      _.ajax.post(_.context.USERS_API, {
        username: this.username(),
        email: this.email(),
        password: this.password(),
        captcha: this.captcha()
      }).then(this.success, this.error);
    };

    this.success = function(data) {
      _.modal('register:complete', data);
    };

    this.error = function(rejection) {
      if (rejection.status === 400) {
        _.alert.error(gettext("Form contains errors."));
        $.extend(self.errors, rejection);
      } else {
        _.ajax.error(rejection);
      }
    };
  };

  Misago.addService('form:register', function(_) {
    _.form('register', Register);
  },
  {
    after: 'forms'
  });
} (Misago.prototype));
