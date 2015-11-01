(function (Misago) {
  'use strict';

  var RequestLink = function(options, _) {
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
      _.api.endpoint('auth').endpoint(options.endpoint).post({
        email: self.email()
      }).then(function(user) {
        self.success(user);
      }, function(error) {
        self.error(error);
      });
    };

    this.success = function(user) {
      options.success(user);
    };

    this.error = function(rejection) {
      if (rejection.status === 400) {
          options.error(rejection, _);
      } else if (rejection.status === 403 && rejection.ban) {
        _.router.error403({
          message: '',
          ban: rejection.ban
        });
      } else {
        _.api.alert(rejection);
      }
    };

    this.reset = function() {
      this.email('');
      options.reset();
    };
  };

  Misago.addService('form:request-link', function(_) {
    _.form('request-link', RequestLink);
  },
  {
    after: 'forms'
  });
} (Misago.prototype));
