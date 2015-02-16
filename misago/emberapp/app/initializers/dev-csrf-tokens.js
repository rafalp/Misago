import Ember from 'ember';
import getCsrfToken from 'misago/utils/csrf';
import ENV from '../config/environment';

export function initialize() {
  if (ENV.environment !== 'production') {
    // set CSRF tokens on preloaded forms
    Ember.$('input[name=csrfmiddlewaretoken]').val(getCsrfToken());
  }
}

export default {
  name: 'dev-csrf-tokens',
  initialize: initialize
};
