import misago from 'misago/index';
import auth from 'misago/services/auth';
import store from 'misago/services/store';
import storage from 'misago/services/local-storage';

export default function initializer() {
  auth.init(store, storage);
}

misago.addInitializer({
  name: 'auth',
  initializer: initializer,
  after: 'store'
});