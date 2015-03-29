import PreloadStore from 'misago/services/preload-store';

export function initialize(container, application) {
  application.register('misago:settings', PreloadStore.get('misagoSettings'), { instantiate: false });
  [ 'route', 'controller', 'component' ].forEach((factory) => {
    application.inject(factory, 'settings', 'misago:settings');
  });

  application.register('misago:static-url', PreloadStore.get('staticUrl'), { instantiate: false });
  application.register('misago:media-url', PreloadStore.get('mediaUrl'), { instantiate: false });

  [ 'controller', 'component' ].forEach((factory) => {
    application.inject(factory, 'staticUrl', 'misago:static-url');
    application.inject(factory, 'mediaUrl', 'misago:media-url');
  });
}

export default {
  name: 'misago-settings',
  initialize: initialize
};
