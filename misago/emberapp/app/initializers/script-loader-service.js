import ScriptLoader from 'misago/services/script-loader';

export function initialize(container, application) {
  application.register('service:script-loader', ScriptLoader, { singleton: true });
  application.inject('service:script-loader', 'staticUrl', 'misago:static-url');
}

export default {
  name: 'script-loader-service',
  after: 'misago-settings',
  initialize: initialize
};
