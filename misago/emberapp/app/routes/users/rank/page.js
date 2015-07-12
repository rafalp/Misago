import IndexRoute from 'misago/routes/users/rank/index';

export default IndexRoute.extend({
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

  actions: {
    didTransition: function() {
      this.set('title', {
        title: this.modelFor('users.rank').get('name'),
        parent: gettext('Users')
      });
    }
  }
});
