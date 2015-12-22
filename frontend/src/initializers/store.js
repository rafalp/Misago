import misago from 'misago/index';
import store from 'misago/services/store';

export default function initalizer() {
  store.init();
}

misago.addInitializer({
  name: 'store',
  initalizer: initalizer,
  before: '_end'
});
