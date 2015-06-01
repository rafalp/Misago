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
    this.get('_modelUnsorted').forEach(function(item) {
      item.unloadRecord();
    });
  }.on('willDestroyElement')
});
