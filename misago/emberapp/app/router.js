import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route("terms_of_service", { path: 'terms-of-service/' });
  this.route("privacy_policy", { path: 'privacy-policy/' });
});

export default Router;
