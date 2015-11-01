(function (Misago) {
  'use strict';

  var LocalStore = function() {
    var storage = window.localStorage;
    var prefix = '_misago_';
    var watchers = [];

    var handleStorageEvent = function(e) {
      var newValueJson = JSON.parse(e.newValue);
      $.each(watchers, function(i, watcher) {
        if (watcher.keyName === e.key && e.oldValue !== e.newValue) {
          watcher.callback(newValueJson);
        }
      });
    };

    window.addEventListener('storage', handleStorageEvent);

    var prefixKey = function(keyName) {
      return prefix + keyName;
    };

    this.set = function(keyName, value) {
      storage.setItem(prefixKey(keyName), JSON.stringify(value));
    };

    this.get = function(keyName) {
      var itemString = storage.getItem(prefixKey(keyName));
      if (itemString) {
        return JSON.parse(itemString);
      } else {
        return null;
      }
    };

    this.watch = function(keyName, callback) {
      watchers.push({keyName: prefixKey(keyName), callback: callback});
    };

    this.destroy = function() {
      this.watchers = [];
    };
  };

  Misago.addService('localstore', {
    factory: function() {
      return new LocalStore();
    },
    destroy: function(_) {
      _.localstore.destroy();
    }
  });
}(Misago.prototype));
