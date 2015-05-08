import Ember from 'ember';

export default Ember.Service.extend({
  _storage: window.localStorage,
  _prefix: '_misago_',
  _watchers: null,

  _initWatches: function() {
    this.set('_watchers', []);

    var self = this;
    window.addEventListener('storage', function(e) {
      self._handleStorageEvent(e);
    });
  }.on('init'),

  _handleStorageEvent: function(e) {
    Ember.$.each(this.get('_watchers'), function(i, watcher) {
      if (watcher.keyName === e.key) {
        watcher.callback(e.newValue);
      }
    });
  },

  prefixKey: function(keyName) {
    return this.get('_prefix') + keyName;
  },

  setItem: function(keyName, value) {
    this.get('_storage').setItem(this.prefixKey(keyName), JSON.stringify(value));
  },

  getItem: function(keyName) {
    var itemJson = this.get('_storage').getItem(this.prefixKey(keyName));
    if (itemJson) {
      return JSON.parse(itemJson);
    } else {
      return null;
    }
  },

  watchItem: function(keyName, callback) {
    this.get('_watchers').push({keyName: this.prefixKey(keyName), callback: callback});
  }
});
