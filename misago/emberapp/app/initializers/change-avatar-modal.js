import ChangeAvatarModal from 'misago/services/change-avatar-modal';

export function initialize(container, application) {
  application.register('service:change-avatar-modal', ChangeAvatarModal, { singleton: true });

  application.inject('service:change-avatar-modal', 'auth', 'service:auth');
}

export default {
  name: 'change-avatar-modal',
  after: 'auth-service',
  initialize: initialize
};
