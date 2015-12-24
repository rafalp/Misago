import { connect } from 'react-redux';
import misago from 'misago/index';
import { UserMenu, select } from 'misago/components/user-menu/root';
import mount from 'misago/utils/mount-component';

export default function initializer() {
  mount(connect(select)(UserMenu), 'user-menu-mount');
}

misago.addInitializer({
  name: 'component:user-menu',
  initializer: initializer,
  after: 'store'
});
