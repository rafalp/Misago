window.Misago = Ember.Application.create({
  rootElement: '#main'
});

Ember.Application.initializer({
  name: 'misago-env',

  initialize: function(container, application) {
    application.register('misago-env:static', MisagoPreloadStore.get('staticUrl'), { instantiate: false });
    application.inject('controller', 'staticUrl', 'misago-env:static');

    application.register('misago-env:media', MisagoPreloadStore.get('mediaUrl'), { instantiate: false });
    application.inject('controller', 'mediaUrl', 'misago-env:media');

    application.register('misago-env:settings', MisagoPreloadStore.get('misago_settings'), { instantiate: false });
    application.inject('controller', 'settings', 'misago-env:settings');
  }
});
