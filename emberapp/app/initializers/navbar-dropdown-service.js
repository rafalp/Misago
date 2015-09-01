export function initialize(container, application) {
  [ 'route', 'component' ].forEach((factory) => {
    application.inject(factory, 'navbar-dropdown', 'service:navbar-dropdown');
  });
}

export default {
  name: 'navbar-dropdown-service',
  initialize: initialize
};
