import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  beforeModel: function() {
    this.store.unloadAll('user');
  },

  model: function() {
    return this.store.find('user', {
      'list': 'rank',
      'rank': this.modelFor('users.rank').get('slug')
    });
  },

  templateName: 'users/rank/index',
  setupController: function(controller, model) {
    var routeName = this.get('templateName').replace(/\//g, '.');
    if (this.get('page') > 1) {
      routeName = routeName.replace('.index', '.page');
    }

    this.controllerFor(routeName).setProperties({
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
