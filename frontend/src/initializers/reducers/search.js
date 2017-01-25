import misago from 'misago';
import reducer, { initialState } from 'misago/reducers/search';
import store from 'misago/services/store';

export default function initializer() {
  store.addReducer('search', reducer, Object.assign({}, initialState, {
    providers: misago.get('SEARCH_PROVIDERS') || []
  }));
}

misago.addInitializer({
  name: 'reducer:search',
  initializer: initializer,
  before: 'store'
});
