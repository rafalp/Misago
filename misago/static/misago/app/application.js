window.Misago = Ember.Application.create({
  rootElement: '#main'
});


Ember.Application.initializer({
  name: 'misago-conf',

  initialize: function(container, application) {
    application.register('misago-conf:static-url', MisagoPreloadStore.get('staticUrl'), { instantiate: false });
    application.inject('controller', 'staticUrl', 'misago-conf:static-url');

    application.register('misago-conf:media-url', MisagoPreloadStore.get('mediaUrl'), { instantiate: false });
    application.inject('controller', 'mediaUrl', 'misago-conf:media-url');

    application.register('misago-conf:settings', MisagoPreloadStore.get('misago_settings'), { instantiate: false });
    application.inject('controller', 'settings', 'misago-conf:settings');
  }
});
