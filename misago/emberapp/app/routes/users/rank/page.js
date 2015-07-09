import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  page: 0,

  model: function(params, transition) {
    var page = this.cleanPage(params.page, transition);
    if (page) {
      this.set('page', page);

      return this.store.find('user', {
        'list': 'rank',
        'rank': this.modelFor('users.rank').get('slug'),
        'page': this.get('page')
      });
    }
  },

  templateName: 'users/rank',
  setupController: function(controller, model) {
    this.controllerFor('users.rank').setProperties({
      'rank': this.modelFor('users.rank'),
      'model': model,
      'meta': model.get("content.meta")
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
