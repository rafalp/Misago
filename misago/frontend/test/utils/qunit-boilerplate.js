(function () {
  'use strict';

  m.deps(window.mock());

  // Boilerplate QUnit acceptance test
  QUnit.acceptance = function(name, conf) {
    var title = document.title;

    var wrappedBeforeEach = conf.beforeEach;
    conf.beforeEach = function() {
      resetTestPromise();

      var modal = document.getElementById('modal-mount');
      $(modal).off();

      if (wrappedBeforeEach) {
        wrappedBeforeEach();
      }
    };

    var wrappedAfterEach = conf.afterEach;
    conf.afterEach = function(assert) {
      var cleaned = assert.async();
      var modal = document.getElementById('modal-mount');

      wrappedAfterEach();

      document.title = title;

      $.mockjax.clear();

      if(!$(modal).hasClass('in')) {
        window.setTimeout(cleaned, 300);
      } else {
        $(modal).on('hidden.bs.modal', function () {
          window.setTimeout(cleaned, 50);
        });
      }

      $(modal).modal('hide');
    };

    QUnit.module('Acceptance: ' + name, conf);
  };
}());
