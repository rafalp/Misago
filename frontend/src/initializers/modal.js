import misago from 'misago/index';
import modal from 'misago/services/modal';

export default function initalizer() {
  let element = document.getElementById('modal-mount');
  if (element) {
    modal.init(element);
  }
}

misago.addInitializer({
  name: 'modal',
  initalizer: initalizer,
  before: 'store'
});
