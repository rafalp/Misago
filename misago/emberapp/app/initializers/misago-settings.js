import PreloadStore from 'misago/services/preload-store';

export function initialize(container, application) {
  application.register('misago:settings', PreloadStore.get('misagoSettings'), { instantiate: false });
  application.inject('route', 'settings', 'misago:settings');
  application.inject('controller', 'settings', 'misago:settings');

  application.register('misago:static-url', PreloadStore.get('staticUrl'), { instantiate: false });
  application.inject('controller', 'staticUrl', 'misago:static-url');

  application.register('misago:media-url', PreloadStore.get('mediaUrl'), { instantiate: false });
  application.inject('controller', 'mediaUrl', 'misago:media-url');
}

export default {
  name: 'misago-settings',
  initialize: initialize
};
