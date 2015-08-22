import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  beforeModel: function() {
    this.store.unloadAll('user');
  },

  model: function() {
    return this.store.find('user', {
      'list': 'online'
    });
  },

  actions: {
    didTransition: function() {
      this.set('title', {
        title: gettext('Online'),
        parent: gettext('Users')
      });
    }
  }
});
