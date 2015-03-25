import Ember from 'ember';
import { initialize } from 'misago/initializers/misago-settings';
import PreloadStore from 'misago/services/preload-store';
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

  assert.equal(container.lookup('misago:static-url'), PreloadStore.get('staticUrl'));
  assert.equal(container.lookup('misago:media-url'), PreloadStore.get('mediaUrl'));
  assert.equal(container.lookup('misago:settings'), PreloadStore.get('misagoSettings'));
});

