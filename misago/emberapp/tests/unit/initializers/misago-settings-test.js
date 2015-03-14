import Ember from 'ember';
import { initialize } from 'misago/initializers/misago-settings';
import MisagoPreloadStore from 'misago/utils/preloadstore';
import { module, test } from 'qunit';

var container, application;

module('SettingsInitializer', {
  beforeEach: function() {
    Ember.run(function() {
      application = Ember.Application.create();
      container = application.__container__;
      application.deferReadiness();
    });
  }
});

test('registers preloaded configuration in Ember', function(assert) {
  assert.expect(3);

  initialize(container, application);

  assert.equal(container.lookup('misago:static-url'), MisagoPreloadStore.get('staticUrl'));
  assert.equal(container.lookup('misago:media-url'), MisagoPreloadStore.get('mediaUrl'));
  assert.equal(container.lookup('misago:settings'), MisagoPreloadStore.get('misagoSettings'));
});

