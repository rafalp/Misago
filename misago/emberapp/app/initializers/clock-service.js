export function initialize(container, application) {
  application.inject('controller', 'clock', 'service:clock');
}

export default {
  name: 'clock-service',
  initialize: initialize
};
