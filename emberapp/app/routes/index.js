import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  actions: {
    didTransition: function() {
      document.title = this.get('settings.forum_index_title') || this.get('settings.forum_name');
    }
  }
});
