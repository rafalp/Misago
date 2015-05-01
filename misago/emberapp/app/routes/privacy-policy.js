import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  page: 'privacy-policy',
  defaultTitle: gettext('Privacy policy'),

  setting: function() {
    return this.get('page').replace(/-/g, '_');
  }.property('page'),

  title: function() {
    return this.get('settings.' + this.get('setting') + '_title') || this.get('defaultTitle');
  }.property('defaultTitle', 'settings'),

  link: function() {
    return this.get('settings.' + this.get('setting') + '_link');
  }.property('settings'),

  beforeModel: function(transition) {
    if (this.get('link')) {
      transition.abort();
      window.location.replace(this.get('link'));
    }
  },

  model: function() {
    return this.store.find('legal-page', this.get('page'));
  },

  afterModel: function(model, transition) {
    if (model.get('link')) {
      transition.abort();
      window.location.replace(model.get('link'));
    }
  },

  actions: {
    didTransition: function() {
      this.set('title', this.get('title'));
    }
  }
});
