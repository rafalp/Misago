import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'last-username-changes',

  isLoaded: false,

  _modelUnsorted: null,
  sorting: ['intId:desc'],
  model: Ember.computed.sort('_modelUnsorted', 'sorting'),

  loadNamechanges: function() {
    var self = this;
    this.store.filter('username-change', { user: this.get('auth.user.id') }, function(change) {
      return change.get('user.id') === self.get('auth.user.id');
    }).then(function(changes) {
      if (self.isDestroyed) { return; }
      self.setProperties({
        '_modelUnsorted': changes,
        'isLoaded': true
      });
    });
  }.on('didInsertElement'),

  unloadNamechanges: function() {
    this.store.unloadAll('username-change');
    this.store.unloadAll('user');
  }.on('willDestroyElement')
});
