import ZxcvbnService from 'misago/services/zxcvbn';

export function initialize(container, application) {
  application.register('service:zxcvbn', ZxcvbnService, { singleton: true });

  application.inject('service:zxcvbn', 'loader', 'service:script-loader');
}

export default {
  name: 'zxcvbn-service',
  after: 'script-loader-service',
  initialize: initialize
};
