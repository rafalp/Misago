import Ember from 'ember';
import ResetScroll from 'misago/mixins/reset-scroll';

export default Ember.Route.extend(ResetScroll, {
  actions: {
    didTransition: function() {
      // Not found route transitions to error404
      throw {status: 404};
    }
  }
});
