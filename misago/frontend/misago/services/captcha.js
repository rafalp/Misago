/* global grecaptcha */
(function (Misago) {
  'use strict';

  var NoCaptcha = function() {
    var deferred = m.deferred();
    deferred.resolve();

    this.load = function() {
      return deferred.promise;
    };

    this.value = function() {
      return null;
    };
  };

  var QACaptcha = function(_) {
    var self = this;

    this.loading = false;
    this.question = null;
    this.value = m.prop('');

    var deferred = m.deferred();
    this.load = function() {
      this.value('');

      if (!this.question && !this.loading) {
        this.loading = true;

        _.api.endpoint('captcha-question').get().then(function(question) {
          self.question = question;
          deferred.resolve();
        }, function() {
          _.ajax.alert(gettext('Failed to load CAPTCHA.'));
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

  var ReCaptcha = function(_) {
    this.included = false;
    this.question = null;

    var deferred = m.deferred();

    var wait = function(promise) {
      if (typeof grecaptcha !== "undefined") {
        promise.resolve();
      } else {
        _.runloop.runOnce(function() {
          wait(promise);
        }, 'loading-grecaptcha', 150);
      }
    };

    this.load = function() {
      if (typeof grecaptcha !== "undefined") {
        grecaptcha.reset();
      }

      if (!this.included) {
        _.include('https://www.google.com/recaptcha/api.js', true);
        this.included = true;
      }

      wait(deferred);

      return deferred.promise;
    };

    var controlConfig = function(el, isInit, context) {
      context.retain = true;

      if (!isInit) {
        grecaptcha.render('recaptcha', {
          'sitekey': _.settings.recaptcha_site_key
        });
      }
    };

    this.component = function(kwargs) {
      var control = m('#recaptcha', {
        config: controlConfig
      });

      return _.component('form-group', {
        label: gettext("Security test"),
        labelClass: kwargs.labelClass || null,
        controlClass: kwargs.controlClass || null,
        control: control,
        validation: kwargs.form.errors,
        validationKey: 'captcha'
      });
    };

    this.value = function() {
      if (typeof grecaptcha !== "undefined") {
        return grecaptcha.getResponse();
      } else {
        return '';
      }
    };

    this.clean = function(form) {
      if (!this.value()) {
        form.errors.captcha = [
          gettext('This field is required.')
        ];
      } else {
        form.errors.captcha = true;
      }
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
      if (captcha.component) {
        return captcha.component(kwargs);
      } else {
        return null;
      }
    };

    this.validator = function() {
      if (captcha.validator) {
        return captcha.validator();
      } else {
        return null;
      }
    };

    this.clean = function(form) {
      if (captcha.clean) {
        captcha.clean(form);
      } else {
        form.errors.captcha = true;
      }
    };
  };

  Misago.addService('captcha', function(_) {
    return new Captcha(_);
  },
  {
    after: 'include'
  });
}(Misago.prototype));
