import MisagoRoute from 'misago/routes/misago';
import ResetScroll from 'misago/mixins/reset-scroll';

export default MisagoRoute.extend(ResetScroll, {
  actions: {
    didTransition: function() {
      document.title = this.get('settings.forum_index_title') || this.get('settings.forum_name');
    }
  }
});
