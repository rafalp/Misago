import { connect } from 'react-redux';
import Categories, { select } from 'misago/components/categories/root';
import misago from 'misago/index';
import mount from 'misago/utils/mount-component';

export default function initializer() {
  if (document.getElementById('categories-mount')) {
    mount(connect(select)(Categories), 'categories-mount');
  }
}

misago.addInitializer({
  name: 'component:categories',
  initializer: initializer,
  after: 'store'
});
