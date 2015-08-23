/* global -Misago */
/* exported Misago */
(function () {
  'use strict';

  window.Misago = function() {

    var ns = Object.getPrototypeOf(this);
    var self = this;

    // Preloaded data
    this.preloaded_data = {
      // Empty settings
      SETTINGS: {}
    };

    // Services
    this._services = [];
    this.addService = function(name, factory, order) {
      this._services.push({
        name: name,
        item: factory,
        after: this.get(order, 'after'),
        before: this.get(order, 'before')
      });
    };

    this._initServices = function(services) {
      var ordered_services = new ns.OrderedList(services).order(false);
      ordered_services.forEach(function (item) {
        var factory = null;
        if (item.item.factory !== undefined) {
          factory = item.item.factory;
        } else {
          factory = item.item;
        }

        var service_instance = factory(self);
        if (service_instance) {
          self[item.name] = service_instance;
        }
      });
    };

    this._destroyServices = function(services) {
      var ordered_services = new ns.OrderedList(services).order();
      ordered_services.reverse();
      ordered_services.forEach(function (item) {
        if (item.destroy !== undefined) {
          item.destroy(self);
        }
      });
    };

    this.registerCoreServices = function() {
      this.addService('conf', ns.Conf);
      this.addService('router', ns.RouterFactory);
      this.addService('outlet', ns.Outlet);
    };

    // Component factory
    this.component = function() {
      var arguments_array = [];
      for (var i = 0; i < arguments.length; i += 1) {
        arguments_array.push(arguments[i]);
      }

      if (arguments_array[arguments_array.length - 1] !== this) {
        arguments_array.push(this);
      }

      return m.component.apply(undefined, arguments_array);
    };

    // App ini/destory
    this._outlet = null;
    this.init = function(outlet) {
      this._outlet = outlet || null;
      this._initServices(this._services);
    };

    this.destroy = function() {
      this._destroyServices();
    };
  };
}());

(function (ns) {
  'use strict';

  ns.ForumLayout = {
    view: function(ctrl, _) {
      return [
        _.component(ns.ForumNavbar)
      ];
    }
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  ns.ForumNavbar = {
    view: function(ctrl, _) {
      var desktop_navbar = [];

      if (_.settings.forum_branding_display) {
        desktop_navbar.push(
          m('a.navbar-brand', {href: _.router.url('misago:index')}, [
            m('img', {
              src: _.router.staticUrl('misago/img/site-logo.png'),
              alt: _.settings.forum_name
            }),
            _.settings.forum_branding_text
          ])
        );
      }

      return m('nav.navbar.navbar-default.navbar-static-top[role="navigation"]', [
        m('.container.navbar-full.hidden-xs.hidden-sm', desktop_navbar)
      ]);
    }
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  ns.Conf = function(_) {
    _.settings = _.get(_.preloaded_data, 'SETTINGS', {});
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  ns.Outlet = {
    factory: function(_) {
      if (_._outlet) {
        m.mount(document.getElementById(_._outlet),
                _.component(ns.ForumLayout));
      }
    },

    destroy: function(_) {
      if (_._outlet) {
        m.mount(_._outlet, null);
      }
    }
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  var prefixUrl = function(prefix) {
    return function(url) {
      return prefix + url;
    };
  };

  var Router = function(_) {
    this.base_url = $('base').attr('href');

    this.url = function() {
      return '/'
    }

    // Media/Static url functions
    this.staticUrl = prefixUrl(_.get(_.preloaded_data, 'STATIC_URL', '/'));
    this.mediaUrl = prefixUrl(_.get(_.preloaded_data, 'MEDIA_URL', '/'));
  };

  ns.RouterFactory = function(_) {
    return new Router(_);
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  ns.has = function(obj, key) {
    if (obj !== undefined) {
      return obj.hasOwnProperty(key);
    } else {
      return false;
    }
  };

  ns.get = function(obj, key, value) {
    if (ns.has(obj, key)) {
      return obj[key];
    } else if (value !== undefined) {
      return value;
    } else {
      return undefined;
    }
  };

  ns.pop = function(obj, key, value) {
    var returnValue = ns.get(obj, key, value);
    if (ns.has(obj, key)) {
      delete obj[key];
    }
    return returnValue;
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  ns.OrderedList = function(items) {
    this.is_ordered = false;
    this._items = items || [];

    this.add = function(key, item, order) {
      this._items.push({
        key: key,
        item: item,
        after: ns.get(order, 'after'),
        before: ns.get(order, 'before')
      });
    };

    this.get = function(key, value) {
      for (var i = 0; i < this._items.length; i++) {
        if (this._items[i].key === key) {
          return this._items[i].item;
        }
      }

      return value;
    };

    this.has = function(key) {
      return this.get(key) !== undefined;
    };

    this.values = function() {
      var values = [];
      for (var i = 0; i < this._items.length; i++) {
        values.push(this._items[i].item);
      }
      return values;
    };

    this.order = function(values_only) {
      if (!this.is_ordered) {
        this._items = this._order(this._items);
        this.is_ordered = true;
      }

      if (values_only || typeof values_only === 'undefined') {
        return this.values();
      } else {
        return this._items;
      }
    };

    this._order = function(unordered) {
      // Index of unordered items
      var index = [];
      unordered.forEach(function (item) {
        index.push(item.key);
      });

      // Ordered items
      var ordered = [];
      var ordering = [];

      // First pass: register items that
      // don't specify their order
      unordered.forEach(function (item) {
        if (!item.after && !item.before) {
          ordered.push(item);
          ordering.push(item.key);
        }
      });

      // Second pass: keep iterating items
      // until we hit iterations limit or finish
      // ordering list
      function insertItem(item) {
        var insertAt = -1;
        if (ordering.indexOf(item.key) === -1) {
          if (item.after) {
            insertAt = ordering.indexOf(item.after);
            if (insertAt !== -1) {
              insertAt += 1;
            }
          } else if (item.before) {
            insertAt = ordering.indexOf(item.before);
          }

          if (insertAt !== -1) {
            ordered.splice(insertAt, 0, item);
            ordering.splice(insertAt, 0, item.key);
          }
        }
      }

      var iterations = 200;
      while (iterations > 0 && index.length !== ordering.length) {
        iterations -= 1;
        unordered.forEach(insertItem);
      }

      return ordered;
    };
  };
} (Misago.prototype));
