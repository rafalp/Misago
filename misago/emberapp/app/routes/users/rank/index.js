import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  model: function() {
    return this.store.find('user', {
      'list': 'rank',
      'rank': this.modelFor('users.rank').get('slug')
    });
  },

  templateName: 'users/rank',
  setupController: function(controller, model) {
    this.controllerFor('users.rank').setProperties({
      'rank': this.modelFor('users.rank'),
      'model': model,
      'meta': model.get('meta')
    });
  },

  actions: {
    didTransition: function() {
      this.set('title', {
        title: this.modelFor('users.rank').get('name'),
        parent: gettext('Users')
      });
    }
  }
});
