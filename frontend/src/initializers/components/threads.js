import { paths } from 'misago/components/threads/root';
import misago from 'misago/index';
import mount from 'misago/utils/routed-component';

export default function initializer(context) {
  if (context.has('THREADS') && context.has('CATEGORIES')) {
    mount({
      paths: paths(context.get('user'))
    });
  }
}

misago.addInitializer({
  name: 'component:threads',
  initializer: initializer,
  after: 'store'
});
