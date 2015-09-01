export function initialize(container, application) {
  [ 'controller', 'component' ].forEach((factory) => {
    application.inject(factory, 'clock', 'service:clock');
  });
}

export default {
  name: 'clock-service',
  initialize: initialize
};
