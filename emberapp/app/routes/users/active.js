import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  beforeModel: function() {
    this.store.unloadAll('user');
  },

  model: function() {
    return this.store.find('user', {
      'list': 'active'
    });
  },

  afterModel: function(users) {
    users.forEach(function(model, index) {
      model.set('meta.ranking', index + 1);
    });
  },

  setupController: function(controller, model) {
    this.controllerFor('users.active').setProperties({
      'model': model,
      'meta': model.get('meta')
    });
  },

  actions: {
    didTransition: function() {
      this.set('title', {
        title: gettext('Most Active'),
        parent: gettext('Users')
      });
    }
  }
});
