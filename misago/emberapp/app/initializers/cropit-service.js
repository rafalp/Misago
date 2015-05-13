import CropitService from 'misago/services/cropit';

export function initialize(container, application) {
  application.register('service:cropit', CropitService, { singleton: true });

  application.inject('service:cropit', 'staticUrl', 'misago:static-url');
}

export default {
  name: 'cropit-service',
  after: 'misago-settings',
  initialize: initialize
};
