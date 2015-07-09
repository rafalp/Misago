import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  actions: {
    didTransition: function() {
      this.set('title', {
        title: gettext('Online'),
        parent: gettext('Users')
      });
    }
  }
});
