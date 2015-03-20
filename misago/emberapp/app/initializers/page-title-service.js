import PageTitleService from 'misago/services/page-title';

export function initialize(container, application) {
  application.inject('service:page-title', 'settings', 'misago:settings');

  application.register('service:page-title', PageTitleService, { singleton: true });
  application.inject('route', 'page-title', 'service:page-title');
}

export default {
  name: 'page-title-service',
  after: 'misago-settings',
  initialize: initialize
};
