import AceEditorService from 'misago/services/ace-editor';

export function initialize(container, application) {
  application.register('service:ace-editor', AceEditorService, { singleton: true });

  application.inject('service:ace-editor', 'loader', 'service:script-loader');
}

export default {
  name: 'ace-editor-service',
  after: 'script-loader-service',
  initialize: initialize
};
