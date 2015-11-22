(function (Misago) {
  'use strict';

  var ResetPassword = function(vm, _) {
    var self = this;

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
      _.ajax.post(vm.api, {
        password: self.password()
      }).then(function(user) {
        self.success(user);
      }, function(error) {
        self.error(error);
      });
    };

    this.success = function(user) {
      vm.success(user, _);
    };

    this.error = function(rejection) {
      _.ajax.error(rejection);
    };
  };

  Misago.addService('form:reset-password', function(_) {
    _.form('reset-password', ResetPassword);
  },
  {
    after: 'forms'
  });
} (Misago.prototype));
