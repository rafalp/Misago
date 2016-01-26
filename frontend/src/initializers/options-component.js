import { Options, paths } from 'misago/components/options/root';
import misago from 'misago/index';
import store from 'misago/services/store';
import mount from 'misago/utils/routed-component';

export default function initializer(context) {
  if (context.get('USER_OPTIONS')) {
    mount({
      root: misago.get('USERCP_URL'),
      component: Options,
      paths: paths(store)
    });
  }
}

misago.addInitializer({
  name: 'component:options',
  initializer: initializer,
  after: 'store'
});
