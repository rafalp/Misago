import Ember from 'ember';
import ResetScroll from 'misago/mixins/reset-scroll';

export default Ember.Route.extend(ResetScroll, {
  actions: {
    didTransition: function() {
      document.title = this.get('settings.forum_index_title') || this.get('settings.forum_name');
    }
  }
});
