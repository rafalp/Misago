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
    var newValueJson = JSON.parse(e.newValue);
    Ember.$.each(this.get('_watchers'), function(i, watcher) {
      if (watcher.keyName === e.key && e.oldValue !== e.newValue) {
        watcher.callback(newValueJson);
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
    var itemString = this.get('_storage').getItem(this.prefixKey(keyName));
    if (itemString) {
      return JSON.parse(itemString);
    } else {
      return null;
    }
  },

  watchItem: function(keyName, callback) {
    this.get('_watchers').push({keyName: this.prefixKey(keyName), callback: callback});
  }
});
