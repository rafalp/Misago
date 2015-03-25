import PreloadStore from 'misago/services/preload-store';
import Auth from 'misago/services/auth';

export function initialize(container, application) {
  var auth = Auth.create({
    'isAuthenticated': PreloadStore.get('isAuthenticated'),
    'user': PreloadStore.get('user')
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
