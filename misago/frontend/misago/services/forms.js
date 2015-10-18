(function (Misago) {
  'use strict';

  var boilerplate = function(form) {
    var _submit = form.submit;
    var _success = form.success;
    var _error = form.error;

    form.isBusy = false;

    form.errors = null;

    form.submit = function() {
      if (form.isBusy) {
        return false;
      }

      if (form.clean) {
        if (form.clean()) {
          form.isBusy = true;
          _submit.apply(form);
        }
      } else {
        form.isBusy = true;
      }
      return false;
    };

    form.success = function() {
      m.startComputation();

      _success.apply(form, arguments);
      form.isBusy = false;

      m.endComputation();
    };

    form.error = function() {
      m.startComputation();

      _error.apply(form, arguments);
      form.isBusy = false;

      m.endComputation();
    };

    form.hasErrors = function() {
      if (form.errors === null) {
        return false;
      }

      for (var key in form.validation) {
        if (form.validation.hasOwnProperty(key)) {
          if (form.errors[key] !== true) {
            return true;
          }
        }
      }

      return false;
    };

    return form;
  };

  var form = function(name, constructor) {
    if (this._forms[name]) {
      if (constructor) {
        return boilerplate(new this._forms[name](constructor, this));
      } else {
        return boilerplate(new this._forms[name](this));
      }
    } else {
      this._forms[name] = constructor;
    }
  };

  Misago.addService('forms', function(_) {
    _._forms = {};
    _.form = form;
  });
}(Misago.prototype));
