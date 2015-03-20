import ZxcvbService from 'misago/services/zxcvb';

export function initialize(container, application) {
  application.register('service:zxcvb', ZxcvbService, { singleton: true });
}

export default {
  name: 'zxcvb-service',
  initialize: initialize
};
