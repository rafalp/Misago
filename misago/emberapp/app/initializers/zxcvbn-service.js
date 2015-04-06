import ZxcvbnService from 'misago/services/zxcvbn';

export function initialize(container, application) {
  application.register('service:zxcvbn', ZxcvbnService, { singleton: true });

  application.inject('service:zxcvbn', 'staticUrl', 'misago:static-url');
}

export default {
  name: 'zxcvbn-service',
  initialize: initialize
};
