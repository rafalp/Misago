(function (Misago) {
  'use strict';

  var MockContainer = function(context) {
    this.context = context;
  };

  QUnit.module("Conf service");

  QUnit.test("preloaded configuration was stored on container", function(assert) {
    var settings = {
      'forum_name': 'Misago Community'
    };

    var container = new MockContainer({SETTINGS: settings});
    Misago.Conf(container);

    assert.equal(container.settings, settings, "service has set preloaded config as settings attribute on container.");
  });
}(Misago.prototype));
