import MisagoPreloadStore from 'misago/utils/preloadstore';

export function initialize(container, application) {
  application.register('misago:preload-store', MisagoPreloadStore, { instantiate: false });
  application.inject('route', 'preloadStore', 'misago:preload-store');
}

export default {
  name: 'misago-preloaded-data',
  initialize: initialize
};
