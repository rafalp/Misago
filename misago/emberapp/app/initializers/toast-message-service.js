import ToastMessageService from 'misago/services/toast-message';

export function initialize(_container, application) {
  application.register('service:toast-message', ToastMessageService, { singleton: true });

  [ 'route', 'controller', 'component' ].forEach((factory) => {
    application.inject(factory, 'toast', 'service:toast-message');
  });
}

export default {
  name: 'toast-message-service',
  initialize: initialize
};
