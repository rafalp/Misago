import AjaxService from 'misago/services/ajax';

export function initialize(_container, application) {
  application.register('service:ajax', AjaxService, { singleton: true });

  application.inject('service:ajax', 'store', 'store:main');

  [ 'route', 'controller', 'component' ].forEach((factory) => {
    application.inject(factory, 'ajax', 'service:ajax');
  });
}

export default {
  name: 'ajax-service',
  initialize: initialize
};
