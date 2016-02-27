import { connect } from 'react-redux';
import Categories, { select } from 'misago/components/categories/root';
import misago from 'misago/index';
import mount from 'misago/utils/mount-component';

export default function initializer(context) {
  if (context.has('CATEGORIES')) {
    mount(connect(select)(Categories), 'page-mount');
  }
}

misago.addInitializer({
  name: 'component:reset-password-form',
  initializer: initializer,
  after: 'store'
});
