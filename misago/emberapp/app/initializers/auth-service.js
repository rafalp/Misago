import MisagoPreloadStore from 'misago/utils/preloadstore';
import Auth from 'misago/services/auth';

export function initialize(container, application) {
  var auth = Auth.create({
    'isAuthenticated': MisagoPreloadStore.get('isAuthenticated'),
    'user': MisagoPreloadStore.get('user')
  });

  application.register('misago:auth', auth, { instantiate: false });
  application.inject('route', 'auth', 'misago:auth');
  application.inject('controller', 'auth', 'misago:auth');

  application.register('misago:user', auth.get('user'), { instantiate: false });
  application.inject('route', 'user', 'misago:user');
  application.inject('controller', 'user', 'misago:user');

}

export default {
  name: 'auth-service',
  initialize: initialize
};
