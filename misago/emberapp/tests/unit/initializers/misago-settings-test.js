import Ember from 'ember';
import { initialize } from 'misago/initializers/misago-settings';
import MisagoPreloadStore from 'misago/utils/preloadstore';

var container, application;

module('SettingsInitializer', {
  setup: function() {
    Ember.run(function() {
      application = Ember.Application.create();
      container = application.__container__;
      application.deferReadiness();
    });
  }
});

test('registers preloaded configuration in Ember', function() {
  initialize(container, application);

  equal(container.lookup('misago:static-url'), MisagoPreloadStore.get('staticUrl'));
  equal(container.lookup('misago:media-url'), MisagoPreloadStore.get('mediaUrl'));
  equal(container.lookup('misago:settings'), MisagoPreloadStore.get('misagoSettings'));
});

