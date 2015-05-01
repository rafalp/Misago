import Ember from 'ember';
import PreloadStore from 'misago/services/preload-store';
import Auth from 'misago/services/auth';

export function initialize(container, application) {
  application.register('service:auth', Auth, { singleton: true });

  application.inject('isAuthenticated', PreloadStore.get('isAuthenticated'), 'service:auth');
  application.inject('user', Ember.Object.create(PreloadStore.get('user')), 'service:auth');

  application.inject('route', 'auth', 'service:auth');
  application.inject('controller', 'auth', 'service:auth');
  application.inject('component', 'auth', 'service:auth');
}

export default {
  name: 'auth-service',
  initialize: initialize
};
