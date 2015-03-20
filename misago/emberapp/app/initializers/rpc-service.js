import RpcService from 'misago/services/rpc';

export function initialize(_container, application) {
  application.register('service:rpc', RpcService, { singleton: true });

  application.inject('service:rpc', 'store', 'store:main');

  [ 'route', 'controller' ].forEach((factory) => {
    application.inject(factory, 'rpc', 'service:rpc');
  });
}

export default {
  name: 'rpc-service',
  initialize: initialize
};
