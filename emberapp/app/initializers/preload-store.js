import PreloadStore from 'misago/services/preload-store';

export function initialize(container, application) {
  application.register('service:preload-store', PreloadStore, { instantiate: false });

  application.inject('route', 'preloadStore', 'service:preload-store');
}

export default {
  name: 'preload-store',
  initialize: initialize
};
