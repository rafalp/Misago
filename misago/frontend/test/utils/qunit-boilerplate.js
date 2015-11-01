(function () {
  'use strict';

  // Boilerplate QUnit acceptance test
  QUnit.acceptance = function(name, conf) {
    var title = document.title;

    var wrappedBeforeEach = conf.beforeEach;
    conf.beforeEach = function() {
      resetTestPromise();
      m.deps(window.mock());
      if (wrappedBeforeEach) {
        wrappedBeforeEach();
      }
    };

    var wrappedAfterEach = conf.afterEach;
    conf.afterEach = function(assert) {
      var cleaned = assert.async();
      wrappedAfterEach();
      document.title = title;
      $.mockjax.clear();

      window.onCleanUp(function() {
        cleaned();
      });
    };

    QUnit.module('Acceptance: ' + name, conf);
  };
}());
