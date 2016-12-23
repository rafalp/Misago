import { paths } from 'misago/components/threads/root';
import misago from 'misago/index';
import mount from 'misago/utils/routed-component';

const PRIVATE_THREADS_LIST = 'misago:private-threads';

export default function initializer(context) {
  if (context.has('THREADS') && context.has('CATEGORIES')) {
    mount({
      paths: paths(context.get('user'), getListOptions(context))
    });
  }
}

export function getListOptions(context) {
  const currentLink = context.get('CURRENT_LINK');
  if (currentLink.substr(0, PRIVATE_THREADS_LIST.length) === PRIVATE_THREADS_LIST) {
    return {
      'api': context.get('PRIVATE_THREADS_API'),
      'title': gettext("Private threads")
    };
  }

  return {
    'api': context.get('THREADS_API')
  };
}

misago.addInitializer({
  name: 'component:threads',
  initializer: initializer,
  after: 'store'
});
