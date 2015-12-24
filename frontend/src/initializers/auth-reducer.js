import misago from 'misago/index';
import reducer from 'misago/reducers/auth';
import store from 'misago/services/store';

export default function initializer(context) {
  store.addReducer('auth', reducer, {
    'isAuthenticated': context.get('isAuthenticated'),
    'isAnonymous': !context.get('isAuthenticated'),

    'user': context.get('user')
  });
}

misago.addInitializer({
  name: 'reducer:auth',
  initializer: initializer,
  before: 'store'
});
