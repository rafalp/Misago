import CropitService from 'misago/services/cropit';

export function initialize(container, application) {
  application.register('service:cropit', CropitService, { singleton: true });

  application.inject('service:cropit', 'loader', 'service:script-loader');
}

export default {
  name: 'cropit-service',
  after: 'script-loader-service',
  initialize: initialize
};
