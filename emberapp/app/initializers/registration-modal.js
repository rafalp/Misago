import RegistrationModal from 'misago/services/registration-modal';

export function initialize(container, application) {
  application.register('service:registration-modal', RegistrationModal, { singleton: true });

  application.inject('service:registration-modal', 'settings', 'misago:settings');
}

export default {
  name: 'registration-modal',
  initialize: initialize
};
