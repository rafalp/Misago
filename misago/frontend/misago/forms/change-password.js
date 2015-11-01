(function (Misago) {
  'use strict';

  var ChangePassword = function(_) {
    var self = this;

    this.username = null;
    this.password = m.prop('');

    this.validation = {
      'password': [
        Misago.validators.passwordMinLength(_.settings)
      ]
    };

    this.clean = function() {
      if (!_.validate(this)) {
        if ($.trim(this.password()).length) {
          _.alert.error(this.errors.password);
        } else {
          _.alert.error(gettext("Enter new password."));
        }
        return false;
      } else {
        return true;
      }
    };

    this.submit = function() {
      var endpoint = _.api.endpoint('auth').endpoint('change-password');
      endpoint = endpoint.endpoint(m.route.param('user_id'));
      endpoint = endpoint.endpoint(m.route.param('token'));

      endpoint.post({
        password: self.password()
      }).then(function(user) {
        self.success(user);
      }, function(error) {
        self.error(error);
      });
    };

    this.success = function(user) {
      this.username = user.username;
    };

    this.error = function(rejection) {
      if (rejection.status === 403 && rejection.ban) {
        _.router.error403({
          message: '',
          ban: rejection.ban
        });
      } else if (rejection.status === 400) {
        _.alert.error(rejection.detail);
      } else {
        _.api.alert(rejection);
      }
    };
  };

  Misago.addService('form:change-password', function(_) {
    _.form('change-password', ChangePassword);
  },
  {
    after: 'forms'
  });
} (Misago.prototype));
