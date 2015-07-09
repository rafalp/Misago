import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  model: function(params) {
    var ranks = this.store.all('rank').filterBy('slug', params.slug);
    if (ranks.length) {
      return ranks.objectAt(0);
    } else {
      this.throw404();
    }
  },

  afterModel: function(model) {
    if (!model.get('is_tab')) {
      this.throw404();
    }
  }
});
