import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  // Auth
  this.route('activation', { path: 'activation/' }, function() {
    this.route('activate', { path: ':user_id/:token/' });
  });
  this.route('forgotten-password', { path: 'forgotten-password/' }, function() {
    this.route('change-form', { path: ':user_id/:token/' });
  });

  // Options
  this.route('options', { path: 'options/' }, function() {
    this.route('forum', { path: 'forum-options/' });
    this.route('signature', { path: 'edit-signature/' });
    this.route('username', { path: 'change-username/' });
    this.route('password', { path: 'change-password/' }, function() {
      this.route('confirm', { path: ':token/' });
    });
    this.route('email', { path: 'change-email/' }, function() {
      this.route('confirm', { path: ':token/' });
    });
  });

  // Users
  this.route('users', { path: 'users/' }, function() {
    this.route('rank', { path: ':slug/' }, function() {
      this.route('index', { path: '/' });
      this.route('page', { path: ':page/' });
    });
    this.route('online', { path: 'online/' }, function() {
      this.route('index', { path: '/' });
    });
    this.route('active', { path: 'active/' }, function() {
      this.route('index', { path: '/' });
    });
  });

  // User
  this.route('user', { path: 'user/:url_name/' });

  // Legal
  this.route('terms-of-service', { path: 'terms-of-service/' });
  this.route('privacy-policy', { path: 'privacy-policy/' });

  // Error
  this.route('error-0', { path: 'error-0/' });
  this.route('error-403', { path: 'error-403/:reason/' });
  this.route('error-404', { path: 'error-404/' });
  this.route('error-banned', { path: 'banned/:reason/' });
  this.route('not-found', { path: '*path' });
});

export default Router;
