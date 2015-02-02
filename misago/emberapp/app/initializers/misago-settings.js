import MisagoPreloadStore from 'misago/utils/preloadstore';

export function initialize(container, application) {
  application.register('misago:static-url', MisagoPreloadStore.get('staticUrl'), { instantiate: false });
  application.inject('controller', 'staticUrl', 'misago:static-url');

  application.register('misago:media-url', MisagoPreloadStore.get('mediaUrl'), { instantiate: false });
  application.inject('controller', 'mediaUrl', 'misago:media-url');

  application.register('misago:settings', MisagoPreloadStore.get('misagoSettings'), { instantiate: false });
  application.inject('route', 'settings', 'misago:settings');
  application.inject('controller', 'settings', 'misago:settings');
}

export default {
  name: 'misago-settings',
  initialize: initialize
};
