import Ember from 'ember';
import ResetScroll from 'misago/mixins/reset-scroll';

export default Ember.Route.extend(ResetScroll, {
  actions: {
    didTransition: function() {
      this.get('page-title').setIndexTitle();
    }
  }
});
