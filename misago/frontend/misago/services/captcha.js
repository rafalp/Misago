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
      return 'pass';
    };
  };

  var QACaptcha = function(_) {
    this.loading = false;
    this.question = null;
    this.value = m.prop('');

    var deferred = m.deferred();
    this.load = function() {
      this.value('');

      if (!this.question && !this.loading) {
        this.loading = true;

        var self = this;
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

    this.component = function(validation) {
      return _.component('form:row', {
        label: this.question.question,
        helpText: this.question.help_text,
        validation: validation
      });
    };
  };

  var ReCaptcha = function(_) {
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
  };

  var Captcha = function(_) {
    var types = {
      'no': NoCaptcha,
      'qa': QACaptcha,
      're': ReCaptcha
    };

    var captcha = new types[_.settings.captcha_type](_);

    this.load = function() {
      return captcha.load();
    };

    this.component = function() {
      return captcha.component();
    };

    this.value = function() {
      return captcha.value();
    };
  };

  Misago.addService('captcha', function(_) {
    return new Captcha(_);
  },
  {
    after: 'include'
  });
}(Misago.prototype));
