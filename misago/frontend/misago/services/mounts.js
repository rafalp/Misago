(function (Misago) {
  'use strict';

  var addMount = function(name) {
    if (this._mounts.indexOf(name) === -1) {
      this._mounts.push(name);
    }
  };

  Misago.addService('mounts', function(_) {
    // Default monts
    _._mounts = [
      'alert-mount',
      'auth-changed-message-mount',
      'page-component',
      'user-menu-mount',
      'user-menu-compact-mount'
    ];

    // Function for including new mounts
    _.addMount = addMount;

    // List of active mounts, for debugging
    _.activeMounts = {};
  });

  Misago.addService('mount-components', {
    factory: function(_) {
      _._mounts.forEach(function(elementId) {
        var mount = document.getElementById(elementId);
        if (mount) {
          _.activeMounts[elementId] = mount.dataset.componentName;
          m.mount(mount, _.component(mount.dataset.componentName));
        }
      });
    },
    destroy: function() {
      _._mounts.forEach(function(elementId) {
        var mount = document.getElementById(elementId);
        if (mount && mount.hasChildNodes()) {
          m.mount(mount, null);
        }
      });
    }
  },
  {
    before: '_end'
  });
}(Misago.prototype));
