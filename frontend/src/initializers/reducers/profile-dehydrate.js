import misago from 'misago/index';
import { dehydrate } from 'misago/reducers/profile';
import store from 'misago/services/store';

export default function initializer() {
  if (misago.has('PROFILE')) {
    store.dispatch(dehydrate(misago.get('PROFILE')));
  }
}

misago.addInitializer({
  name: 'reducer:profile-dehydrate',
  initializer: initializer,
  after: 'store'
});
