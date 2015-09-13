/* global -Misago */
/* exported Misago */
(function () {
  'use strict';

  window.Misago = function() {
    var ns = Object.getPrototypeOf(this);
    var self = this;

    // Context data
    this.context = {
      // Empty settings
      SETTINGS: {}
    };

    this._initServices = function(services) {
      var orderedServices = new ns.OrderedList(services).order(false);
      orderedServices.forEach(function (item) {
        var factory = null;
        if (item.item.factory !== undefined) {
          factory = item.item.factory;
        } else {
          factory = item.item;
        }

        var serviceInstance = factory(self);
        if (serviceInstance) {
          self[item.key] = serviceInstance;
        }
      });
    };

    this._destroyServices = function(services) {
      var orderedServices = new ns.OrderedList(services).order();
      orderedServices.reverse();
      orderedServices.forEach(function (item) {
        if (item.destroy !== undefined) {
          item.destroy(self);
        }
      });
    };

    // App init/destory
    this.setup = false;
    this.init = function(setup) {
      this.setup = {
        fixture: ns.get(setup, 'fixture', null),
        inTest: ns.get(setup, 'inTest', false)
      };

      this._initServices(ns._services);
    };

    this.destroy = function() {
      this._destroyServices(ns._services);
    };
  };


  // Services
  var proto = window.Misago.prototype
  proto._services = [];

  proto.addService = function(name, factory, order) {
    Misago.prototype._services.push({
      key: name,
      item: factory,
      after: proto.get(order, 'after'),
      before: proto.get(order, 'before')
    });
  };
}());

(function (Misago) {
  'use strict';

  Misago.has = function(obj, key) {
    if (obj !== undefined) {
      return obj.hasOwnProperty(key);
    } else {
      return false;
    }
  };

  Misago.get = function(obj, key, value) {
    if (Misago.has(obj, key)) {
      return obj[key];
    } else if (value !== undefined) {
      return value;
    } else {
      return undefined;
    }
  };

  Misago.pop = function(obj, key, value) {
    var returnValue = Misago.get(obj, key, value);
    if (Misago.has(obj, key)) {
      delete obj[key];
    }
    return returnValue;
  };
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.OrderedList = function(items) {
    this.isOrdered = false;
    this._items = items || [];

    this.add = function(key, item, order) {
      this._items.push({
        key: key,
        item: item,
        after: Misago.get(order, 'after'),
        before: Misago.get(order, 'before')
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
      if (!this.isOrdered) {
        this._items = this._order(this._items);
        this.isOrdered = true;
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

      // Second pass: register items that
      // specify their before to "_end"
      unordered.forEach(function (item) {
        if (item.before === "_end") {
          ordered.push(item);
          ordering.push(item.key);
        }
      });

      // Third pass: keep iterating items
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

(function (Misago) {
  Misago.deserializeDatetime = function(deserialized) {
    return deserialized ? moment(deserialized) : null;
  };

  Misago.serializeDatetime = function(serialized) {
    return serialized ? serialized.format() : null;
  };
} (Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.startsWith = function(string, beginning) {
    return string.indexOf(beginning) === 0;
  };

  Misago.endsWith = function(string, tail) {
    return string.indexOf(tail, string.length - tail.length) !== -1;
  };
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.UrlConfInvalidComponentError = function(name) {
    this.message = "route's " + name + " component should be an array or object";

    this.toString = function() {
      return this.message;
    };
  };

  Misago.UrlConf = function() {
    var self = this;
    this._patterns = [];

    this.patterns = function() {
      return this._patterns;
    };

    var prefixPattern = function(prefix, pattern) {
      return (prefix + pattern).replace('//', '/');
    };

    var include = function(prefix, patterns) {
      for (var i = 0; i < patterns.length; i ++) {
        self.url(prefixPattern(prefix, patterns[i].pattern),
                 patterns[i].component,
                 patterns[i].name);
      }
    };

    this.url = function(pattern, component, name) {
      if (typeof component !== 'object') {
        throw new Misago.UrlConfInvalidComponentError(name);
      }

      if (pattern === '') {
        pattern = '/';
      }

      if (component instanceof Misago.UrlConf) {
        include(pattern, component.patterns());
      } else {
        this._patterns.push({
          pattern: pattern,
          component: component,
          name: name
        });
      }
    };
  };
} (Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.loadingPage = function(_) {
    return m('.page.page-loading', _.component(Misago.Loader));
  };
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var Ajax = function(_) {
    var cookieRegex = new RegExp(_.context.CSRF_COOKIE_NAME + '\=([^;]*)');
    this.csrfToken = Misago.get(document.cookie.match(cookieRegex), 0).split('=')[1];

    /*
      List of GETs underway
      We are limiting number of GETs to API to 1 per url
    */
    var runningGets = {};

    this.ajax = function(method, url, data, progress) {
      var promise = m.deferred();

      var ajax_settings = {
        url: url,
        method: method,
        headers: {
          'X-CSRFToken': this.csrfToken
        },

        data: data | {},
        dataType: 'json',

        success: function(data) {
          if (method === 'GET') {
            Misago.pop(runningGets, url);
          }
          promise.resolve(data);
        },
        error: function(jqXHR) {
          if (method === 'GET') {
            Misago.pop(runningGets, url);
          }

          var rejection = jqXHR.responseJSON || {};

          rejection.status = jqXHR.status;
          rejection.statusText = jqXHR.statusText;

          promise.reject(rejection);
        }
      };

      if (progress) {
        return; // not implemented... yet!
      }

      $.ajax(ajax_settings);
      return promise.promise;
    };

    this.get = function(url) {
      var preloaded = Misago.pop(_.context, url);
      if (preloaded) {
        var deferred = m.deferred();
        deferred.resolve(preloaded);
        return deferred.promise;
      } else if (runningGets[url] !== undefined) {
        return runningGets[url];
      } else {
        runningGets[url] = this.ajax('GET', url);
        return runningGets[url];
      }
    };

    this.post = function(url) {
      return this.ajax('POST', url);
    };
  };

  Misago.addService('ajax', function(_) {
    return new Ajax(_);
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var Api = function(_) {
    this.buildUrl = function(model, call, querystrings) {
      var url = _.router.baseUrl;
      url += 'api/' + model + '/';
      return url;
    };

    this.one = function(model, id) {
      var url = this.buildUrl(model) + id + '/';
      return _.ajax.get(url);
    };

    this.many = function(model, filters) {

    };

    this.call = function(model, target, call, data) {

    };
  };

  Misago.addService('api', function(_) {
    return new Api(_);
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.addService('components-factory', function(_) {
    // Component factory
    _.component = function() {
      var argumentsArray = [];
      for (var i = 0; i < arguments.length; i += 1) {
        argumentsArray.push(arguments[i]);
      }

      argumentsArray.push(_);
      return m.component.apply(undefined, argumentsArray);
    };
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.addService('conf', function(_) {
    _.settings = Misago.get(_.context, 'SETTINGS', {});
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.addService('forum-layout', {
    factory: function(_) {
      if (_.setup.fixture) {
        m.mount(document.getElementById(_.setup.fixture),
                _.component(Misago.ForumLayout));
      }
    },

    destroy: function(_) {
      if (_.setup.fixture) {
        m.mount(_.setup.fixture, null);
      }
    }
  }, {before: 'start-routing'});
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.addService('set-momentjs-locale', function() {
    moment.locale($('html').attr('lang'));
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var noop = function() {};

  Misago.route = function(component) {
    /*
      Boilerplate for Misago top-level components
    */

    // Component state
    component.isActive = true;

    // Wrap controller to store lifecycle methods
    var __controller = component.controller || noop;
    component.controller = function() {
      component.isActive = true;

      var controller = __controller.apply(component, arguments) || {};

      // wrap onunload for lifestate
      var __onunload = controller.onunload || noop;
      controller.onunload = function() {
        __onunload.apply(component, arguments);
        component.isActive = false;
      };

      return controller;
    };

    // Add state callbacks to View-Model
    if (component.vm && component.vm.init) {
      // wrap vm.init in promise handler
      var __init = component.vm.init;
      component.vm.init = function() {
        var initArgs = arguments;
        var promise = __init.apply(component.vm, initArgs);

        if (promise) {
          promise.then(function() {
            if (component.isActive && component.vm.ondata) {
              var finalArgs = [];
              for (var i = 0; i < arguments.length; i++) {
                finalArgs.push(arguments[i]);
              }
              for (var f = 0; f < initArgs.length; f++) {
                finalArgs.push(initArgs[f]);
              }

              component.vm.ondata.apply(component.vm, finalArgs);
            }
          }, function(error) {
            if (component.isActive) {
              component.container.router.errorPage(error);
            }
          });
        }
      };

      // setup default loading view
      if (!component.loading) {
        component.loading = function () {
          var _ = this.container;
          return m('.page.page-loading',
            _.component(Misago.Loader)
          );
        };
      }

      var __view = component.view;
      component.view = function() {
        if (component.vm.isReady) {
          return __view.apply(component, arguments);
        } else {
          return component.loading.apply(component, arguments);
        }
      };
    }

    return component;
  };
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var Router = function(_) {
    var self = this;
    this.baseUrl = $('base').attr('href');

    var staticUrl = Misago.get(_.context, 'STATIC_URL', '/');
    var mediaUrl = Misago.get(_.context, 'MEDIA_URL', '/');

    // Routing
    this.urls = {};
    this.reverses = {};

    var routedComponent = function(component) {
      component.container = _;
      return component;
    };

    var populatePatterns = function(urlconf) {
      urlconf.patterns().forEach(function(url) {
        // set service container on component

        var finalPattern = self.baseUrl + url.pattern;
        finalPattern = finalPattern.replace('//', '/');

        self.urls[finalPattern] = routedComponent(url.component);
        self.reverses[url.name] = finalPattern;
      });
    };

    this.startRouting = function(urlconf, fixture) {
      populatePatterns(urlconf);
      this.fixture = fixture;

      m.route.mode = 'pathname';
      m.route(fixture, '/', this.urls);
    };

    this.url = function(name) {
      return this.reverses[name];
    };

    // Delegate clicks
    this.delegateElement = null;
    this.delegateName = 'click.misago-router';

    this.cleanUrl = function(url) {
      if (!url) { return; }

      // Is link relative?
      var isRelative = url.substr(0, 1) === '/' && url.substr(0, 2) !== '//';

      // If link contains host, validate to see if its outgoing
      if (!isRelative) {
        var location = window.location;

        // If protocol matches current one, strip it from string
        // otherwhise stop handler
        if (url.substr(0, 2) !== '//') {
          var protocol = url.substr(0, location.protocol.length + 2);
          if (protocol !== location.protocol + '//') { return; }
          url = url.substr(location.protocol.length + 2);
        } else {
          url = url.substr(2);
        }

        // Host checks out?
        if (url.substr(0, location.host.length) !== location.host) { return; }
        url = url.substr(location.host.length);
      }

      // Is link within Ember app?
      if (url.substr(0, this.baseUrl.length) !== this.baseUrl) { return; }

      // Is link to media/static/avatar server?
      if (url.substr(0, staticUrl.length) === staticUrl) { return; }

      if (url.substr(0, mediaUrl.length) === mediaUrl) { return; }

      var avatarsUrl = '/user-avatar/';
      if (url.substr(0, avatarsUrl.length) === avatarsUrl) { return; }

      return url;
    };

    this.delegateClicks = function(element) {
      this.delegateElement = element;
      $(this.delegateElement).on(this.delegateName, 'a', function(e) {
        var cleanUrl = self.cleanUrl(e.target.href);
        if (cleanUrl) {
          if (cleanUrl != m.route()) {
            m.route(cleanUrl);
          }
          e.preventDefault();
        }
      });
    };

    this.destroy = function() {
      $(this.delegateElement).off(this.delegateName);
    };

    // Media/Static url
    var prefixUrl = function(prefix) {
      return function(url) {
        return prefix + url;
      };
    };

    this.staticUrl = prefixUrl(staticUrl);
    this.mediaUrl = prefixUrl(mediaUrl);

    // Errors
    this.error403 = function(error) {
      var component = null;
      if (error.ban) {
        component = routedComponent(Misago.ErrorBannedRoute);
        component.error = {
          message: error.detail,
          ban: Misago.Ban.deserialize(error.ban)
        };
      } else {
        component = routedComponent(Misago.Error403Route);
        component.error = error.detail;
      }

      m.mount(this.fixture, component);
    };

    this.error404 = function() {
      m.mount(this.fixture, routedComponent(Misago.Error404Route));
    };

    this.error500 = function() {
      m.mount(this.fixture, routedComponent(Misago.Error500Route));
    };

    this.error0 = function() {
      m.mount(this.fixture, routedComponent(Misago.Error0Route));
    };

    this.errorPage = function(error) {
      if (error.status === 0) {
        this.error0();
      }

      if (error.status === 500) {
        this.error500();
      }

      if (error.status === 404) {
        this.error404();
      }

      if (error.status === 403) {
        this.error403(error);
      }
    };
  };

  Misago.addService('router', function(_) {
    return new Router(_);
  });

  Misago.addService('start-routing', function(_) {
    _.router.startRouting(Misago.urls, document.getElementById('router-fixture'));
    _.router.delegateClicks(document.getElementById(_.setup.fixture));
  }, {before: '_end'});
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var RunLoop = function(_) {
    var self = this;

    this._intervals = {};

    this.run = function(callable, name, delay) {
      this._intervals[name] = window.setTimeout(function() {
        var result = callable(_);
        if (result !== false) {
          self.run(callable, name, delay);
        }
      }, delay);
    };

    this.runOnce = function(callable, name, delay) {
      this._intervals[name] = window.setTimeout(function() {
        callable(_);
      }, delay);
    };

    this.stop = function() {
      for (var name in this._intervals) {
        if (this._intervals.hasOwnProperty(name)) {
          window.clearTimeout(this._intervals[name]);
          delete this._intervals[name];
        }
      }
    };
  };

  Misago.addService('runloop', {
    factory: function(_) {
      return new RunLoop(_);
    },

    destroy: function(_) {
      _.runloop.stop();
    }
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.addService('start-tick', function(_) {
    _.runloop.run(function() {
      m.startComputation();
      // just tick once a minute so stuff gets rerendered
      // syncing dynamic timestamps, etc ect
      m.endComputation();
    }, 'tick', 60000);
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.addService('page-title', function(_) {
    _._setTitle = function(title) {
      if (typeof title === 'string') {
        title = {title: title};
      }

      var completeTitle = title.title;

      if (typeof title.page !== 'undefined' && title.page > 1) {
        completeTitle += ' (' + interpolate(gettext('page %(page)s'), { page:title.page }, true) + ')';
      }

      if (typeof title.parent !== 'undefined') {
        completeTitle += ' | ' + title.parent;
      }

      document.title = completeTitle + ' | ' + this.settings.forum_name;
    };

    _.setTitle = function(title) {
      if (title) {
        this._setTitle(title);
      } else {
        document.title = this.settings.forum_name;
      }
    };
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.Ban = function(data) {
    this.message = {
      html: data.message.html,
      plain: data.message.plain,
    };

    this.expires_on = data.expires_on;
  };

  Misago.Ban.deserialize = function(data) {
    data.expires_on = Misago.deserializeDatetime(data.expires_on);

    return new Misago.Ban(data);
  };
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var errorPage = function(error) {
    var error_message = [
      m('p.lead', error.message)
    ];

    if (error.help) {
      error_message.push(m('p.help', error.help));
    }

    return m('.page.error-page.error-' + error.code + '-page',
      m('.container',
        m('.error-panel', [
          m('.error-icon',
            m('span.material-icon', error.icon)
          ),
          m('.error-message', error_message)
        ])
      )
    );
  };

  Misago.ErrorBannedRoute = Misago.route({
    controller: function() {
      this.container.setTitle(gettext('You are banned'));
    },
    error: null,
    view: function() {
      var error_message = [];
      if (this.error.ban.message.html) {
        error_message.push(m('.lead', m.trust(this.error.ban.message.html)));
      } else {
        error_message.push(m('p.lead', this.error.message));
      }

      var expirationMessage = null;
      if (this.error.ban.expires_on) {
        if (this.error.ban.expires_on.isAfter(moment())) {
          expirationMessage = interpolate(
            gettext('This ban expires %(expires_on)s.'),
            { 'expires_on': this.error.ban.expires_on.fromNow() },
            true);
        } else {
          expirationMessage = gettext('This ban has expired.');
        }
      } else {
        expirationMessage = gettext('This ban is permanent.');
      }
      error_message.push(m('p', expirationMessage));

      return m('.page.error-page.error-banned-page',
        m('.container',
          m('.error-panel', [
            m('.error-icon',
              m('span.material-icon', 'highlight_off')
            ),
            m('.error-message', error_message)
          ])
        )
      );
    }
  });

  Misago.Error403Route = Misago.route({
    controller: function() {
      this.container.setTitle(gettext('Page not available'));
    },
    error: null,
    view: function() {
      return errorPage({
        code: 403,
        icon: 'remove_circle_outline',
        message: gettext("This page is not available."),
        help: this.error || gettext("You don't have permission to access this page.")
      });
    }
  });

  Misago.Error404Route = Misago.route({
    controller: function() {
      this.container.setTitle(gettext('Page not found'));
    },
    view: function() {
      return errorPage({
        code: 404,
        icon: 'info_outline',
        message: gettext("Requested page could not be found."),
        help: gettext("The link you followed was incorrect or the page has been moved or deleted.")
      });
    }
  });

  Misago.Error500Route = Misago.route({
    controller: function() {
      this.container.setTitle(gettext('Application error occured'));
    },
    view: function() {
      return errorPage({
        code: 500,
        icon: 'error_outline',
        message: gettext("Requested page could not be displayed due to an error."),
        help: gettext("Please try again later or contact site staff if error persists.")
      });
    }
  });

  Misago.Error0Route = Misago.route({
    controller: function() {
      this.container.setTitle(gettext('Lost connection with application'));
    },
    view: function() {
      return errorPage({
        code: 500,
        icon: 'sync_problem',
        message: gettext("Could not connect to application."),
        help: gettext("This may be caused by problems with your connection or application server. Please check your internet connection and refresh page if problem persists.")
      });
    }
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.IndexRoute = Misago.route({
    controller: function() {
      var _ = this.container;
      document.title = _.settings.forum_index_title || _.settings.forum_name;

      var count = m.prop(0);

      return {
        count: count,
        increment: function() {
          console.log('increment()');
          count(count() + 1);
        }
      };
    },
    view: function(ctrl) {
      return m('.container', [
        m('h1', ['Count: ', m('strong', ctrl.count())]),
        m('p', 'Clicky click button to increase count!.'),
        m('p',
          m('button.btn.btn-primary', {onclick: ctrl.increment}, 'Clicky clicky!')
        )
      ]);
    }
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var legalPageFactory = function(typeName, defaultTitle) {
    var dashedTypeName = typeName.replace(/_/g, '-');

    return Misago.route({
      controller: function() {
        var _ = this.container;

        if (Misago.get(_.settings, typeName + '_link')) {
          window.location = Misago.get(_.settings, typeName + '_link');
        } else {
          this.vm.init(this, _);
        }
      },
      vm: {
        isReady: false,
        init: function(component, _) {
          if (this.isReady) {
            _.setTitle(this.title);
          } else {
            _.setTitle();
            return _.api.one('legal-pages', dashedTypeName);
          }
        },
        ondata: function(data, component, _) {
          m.startComputation();

          this.title = data.title || defaultTitle;
          this.body = data.body;
          this.isReady = true;

          m.endComputation();

          if (component.isActive) {
            _.setTitle(data.title);
          }
        }
      },
      view: function() {
        var _ = this.container;

        return m('.page.legal-page.' + dashedTypeName + '-page', [
          _.component(Misago.PageHeader, {title: this.vm.title}),
          m('.container',
            m.trust(this.vm.body)
          )
        ]);
      }
    });
  };

  Misago.TermsOfServiceRoute = legalPageFactory(
    'terms_of_service', gettext('Terms of service'));
  Misago.PrivacyPolicyRoute = legalPageFactory(
    'privacy_policy', gettext('Privacy policy'));
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var legalLink = function(_, legalType, defaultTitle) {
    var url = Misago.get(_.settings, legalType + '_link');
    if (!url && Misago.get(_.settings, legalType)) {
      url = _.router.url(legalType);
    }

    if (url) {
      return m('li',
        m('a', {href: url}, Misago.get(_.settings, legalType + '_title', defaultTitle))
      );
    } else {
      return null;
    }
  };

  Misago.FooterNav = {
    isVisible: function(settings) {
      return [
        !!settings.forum_footnote,
        !!settings.terms_of_service,
        !!settings.terms_of_service_link,
        !!settings.privacy_policy,
        !!settings.privacy_policy_link
      ].indexOf(true) !== -1;
    },
    view: function(ctrl, _) {
      var items = [];

      if (_.settings.forum_footnote) {
        items.push(m('li.forum-footnote', m.trust(_.settings.forum_footnote)));
      }

      items.push(legalLink(_, 'terms_of_service', gettext('Terms of service')));
      items.push(legalLink(_, 'privacy_policy', gettext('Privacy policy')));

      return m('ul.list-inline.footer-nav', items);
    }
  };
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.ForumFooter = {
    view: function(ctrl, _) {
      var nav = null;
      if (Misago.FooterNav.isVisible(_.settings)) {
        nav = _.component(Misago.FooterNav);
      }

      return m('footer.forum-footer', [
        m('.container',
          m('.footer-content', [
            nav,
            _.component(Misago.FooterMisagoBranding)
          ])
        )
      ]);
    }
  };
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.FooterMisagoBranding = {
    view: function() {
      return m('a.misago-branding[href=http://misago-project.org]', [
        "powered by ", m('strong', "misago")
      ]);
    }
  };
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.BrandFull = {
    view: function(ctrl, branding, _) {
      var children = [
        m('img', {
          src: _.router.staticUrl('misago/img/site-logo.png'),
          alt: _.settings.forum_name
        })
      ];

      if (branding) {
        children.push(branding);
      }

      return m('a.navbar-brand', {href: _.router.url('index')}, children);
    }
  };
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.ForumNavbar = {
    view: function(ctrl, _) {
      var desktopNavbar = [];

      if (_.settings.forum_branding_display) {
        desktopNavbar.push(_.component(Misago.BrandFull, _.settings.forum_branding_text));
      }

      desktopNavbar.push(m('ul.nav.navbar-nav', [
        m('li', m("a", {config: m.route, href: _.router.url('index')}, 'Index'))
      ]));

      return m('nav.navbar.navbar-default.navbar-static-top[role="navigation"]', [
        m('.container.navbar-full.hidden-xs.hidden-sm', desktopNavbar)
      ]);
    }
  };
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  Misago.ForumLayout = {
    view: function(ctrl, _) {
      return [
        _.component(Misago.ForumNavbar),
        m('#router-fixture', {config: persistent}),
        _.component(Misago.ForumFooter)
      ];
    }
  };
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.Loader = {
    view: function() {
      return m('.loader.sk-folding-cube', [
        m('.sk-cube1.sk-cube'),
        m('.sk-cube2.sk-cube'),
        m('.sk-cube4.sk-cube'),
        m('.sk-cube3.sk-cube')
      ]);
    }
  };

  Misago.LoadingPage = {
    view: function(ctrl, _) {
      return m('.page.loading-page',
        _.component(Misago.Loader)
      );
    }
  };
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var setupMarkup = function(el, isInit, context) {
    context.retain = true;
  };

  Misago.MisagoMarkup = {
    view: function(ctrl, content) {
      return m('article.misago-markup', {config: setupMarkup}, m.trust(content));
    }
  };
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.PageHeader = {
    view: function(ctrl, options) {
      return m('.page-header',
        m('.container', [
          m('h1', options.title),
        ])
      );
    }
  };
}(Misago.prototype));

(function (Misago, UrlConf) {
  'use strict';

  var urls = new UrlConf();
  urls.url('/', Misago.IndexRoute, 'index');

  // Legal pages
  urls.url('/terms-of-service/', Misago.TermsOfServiceRoute, 'terms_of_service');
  urls.url('/privacy-policy/', Misago.PrivacyPolicyRoute, 'privacy_policy');

  Misago.urls = urls;
} (Misago.prototype, Misago.prototype.UrlConf));
