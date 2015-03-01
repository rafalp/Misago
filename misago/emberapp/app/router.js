import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('forgotten-password', { path: 'forgotten-password/' }, function() {
    this.route('change-form', { path: ':user_id/:token/' });
  });
  this.route('terms-of-service', { path: 'terms-of-service/' });
  this.route('privacy-policy', { path: 'privacy-policy/' });
  this.route('error-0', { path: 'error-0/' });
  this.route('error-403', { path: 'error-403/:reason/' });
  this.route('error-404', { path: 'error-404/' });
  this.route('error-banned', { path: 'banned/:reason/' });
  this.route('not-found', { path: '*path' });
});

export default Router;
