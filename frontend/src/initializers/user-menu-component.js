import { connect } from 'react-redux';
import misago from 'misago/index';
import { UserMenu, CompactUserMenu, select } from 'misago/components/user-menu/root';
import mount from 'misago/utils/mount-component';

export default function initializer() {
  mount(connect(select)(UserMenu), 'user-menu-mount');
  mount(connect(select)(CompactUserMenu), 'user-menu-compact-mount');
}

misago.addInitializer({
  name: 'component:user-menu',
  initializer: initializer,
  after: 'store'
});
