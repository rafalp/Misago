import LocalStore from 'misago/services/local-store';

export function initialize(container, application) {
  application.register('store:local', LocalStore, { singleton: true });
}

export default {
  name: 'local-store',
  initialize: initialize
};
