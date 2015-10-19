(function (Misago) {
  'use strict';

  var NoCaptcha = function() {
    var deferred = m.deferred();
    deferred.resolve();

    this.load = function() {
      return deferred.promise;
    };

    this.component = function() {
      return null;
    };

    this.value = function() {
      return null;
    };

    this.validator = function() {
      return null;
    };
  };

  var QACaptcha = function(_) {
    var self = this;

    this.loading = false;
    this.question = null;
    this.value = m.prop('asdsadsa');

    var deferred = m.deferred();
    this.load = function() {
      this.value('');

      if (!this.question && !this.loading) {
        this.loading = true;

        _.api.endpoint('captcha-question').get().then(function(question) {
          self.question = question;
          deferred.resolve();
        }, function() {
          _.api.alert(gettext('Failed to load CAPTCHA.'));
          deferred.reject();
        }).then(function() {
          self.loading = true;
        });
      }

      return deferred.promise;
    };

    this.component = function(kwargs) {
      return _.component('form-group', {
        label: this.question.question,
        labelClass: kwargs.labelClass || null,
        controlClass: kwargs.controlClass || null,
        control: _.input({
          value: _.validate(kwargs.form, 'captcha'),
          id: 'id_captcha',
          disabled: kwargs.form.isBusy
        }),
        validation: kwargs.form.errors,
        validationKey: 'captcha',
        helpText: this.question.help_text
      });
    };

    this.validator = function() {
      return [];
    };
  };

  var ReCaptcha = function() {
    this.loading = false;
    this.question = null;

    var deferred = m.deferred();
    this.load = function() {
      return deferred.promise;
    };

    this.component = function() {
      return 'null';
    };

    this.value = function() {
      return 'pass';
    };

    this.validator = function() {
      return [];
    };
  };

  var Captcha = function(_) {
    var types = {
      'no': NoCaptcha,
      'qa': QACaptcha,
      're': ReCaptcha
    };

    var captcha = new types[_.settings.captcha_type](_);

    this.value = captcha.value;

    this.load = function() {
      return captcha.load();
    };

    this.component = function(kwargs) {
      return captcha.component(kwargs);
    };

    this.validator = function() {
      return captcha.validator();
    };
  };

  Misago.addService('captcha', function(_) {
    return new Captcha(_);
  },
  {
    after: 'include'
  });
}(Misago.prototype));
