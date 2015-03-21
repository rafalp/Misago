import CSRFService from 'misago/services/csrf';

export function initialize(container, application) {
  application.register('service:csrf', CSRFService, { singleton: true });

  application.inject('service:csrf', 'preloadedStore', 'misago:preloaded-data');

  [ 'controller', 'adapter' ].forEach((factory) => {
    application.inject(factory, 'csrf', 'service:csrf');
  });
}

export default {
  name: 'csrf-service',
  initialize: initialize
};
