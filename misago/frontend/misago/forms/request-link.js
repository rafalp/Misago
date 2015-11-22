(function (Misago) {
  'use strict';

  var RequestLink = function(vm, _) {
    var self = this;

    this.email = m.prop('');

    this.validation = {
      'email': [
        Misago.validators.email()
      ]
    };

    this.clean = function() {
      if (!_.validate(this)) {
        _.alert.error(gettext("Enter a valid email address."));
        return false;
      } else {
        return true;
      }
    };

    this.submit = function() {
      _.ajax.post(vm.api, {
        email: self.email()
      }).then(function(user) {
        self.success(user);
      }, function(error) {
        self.error(error);
      });
    };

    this.success = function(user) {
      vm.success(user);
    };

    this.error = function(rejection) {
      if (rejection.status === 400) {
          vm.error(rejection, _);
      } else {
        _.ajax.error(rejection);
      }
    };

    this.reset = function() {
      this.email('');
      vm.reset();
    };
  };

  Misago.addService('form:request-link', function(_) {
    _.form('request-link', RequestLink);
  },
  {
    after: 'forms'
  });
} (Misago.prototype));
