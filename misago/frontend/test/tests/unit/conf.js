(function (ns) {
  'use strict';

  var MockContainer = function(preloaded_data) {
    this.preloaded_data = preloaded_data;
  };

  QUnit.module("Conf service");

  QUnit.test("preloaded configuration was stored on container", function(assert) {
    var settings = {
      'forum_name': 'Misago Community'
    };

    var container = new MockContainer({SETTINGS: settings});
    ns.Conf(container);

    assert.equal(container.settings, settings, "service has set preloaded config as settings attribute on container.");
  });
}(Misago.prototype));
