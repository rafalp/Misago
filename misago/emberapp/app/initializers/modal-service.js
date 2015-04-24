export function initialize(container, application) {
  [ 'route', 'component' ].forEach((factory) => {
    application.inject(factory, 'modal', 'service:modal');
  });
}

export default {
  name: 'modal-service',
  initialize: initialize
};
