import Ember from 'ember';

export default Ember.Route.extend({
  actions: {
    didTransition: function() {
      // Not found route transitions to error404
      throw {status: 404};
    }
  }
});
