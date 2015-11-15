/* global -Misago */
/* exported Misago */
(function () {
  'use strict';

  window.Misago = function() {
    var ns = Object.getPrototypeOf(this);
    var self = this;

    // Services init/destroy
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

    // Context data
    this.context = {
      // Empty settings
      SETTINGS: {}
    };

    // App init/destory
    this.setup = false;
    this.init = function(setup, context) {
      this.setup = {
        test: ns.get(setup, 'test', false),
        api: ns.get(setup, 'api', '/api/')
      };

      if (context) {
        this.context = context;
      }

      this._initServices(ns._services);
    };

    this.destroy = function() {
      this._destroyServices(ns._services);
    };
  };

  // Services
  var proto = window.Misago.prototype;

  proto._services = [];
  proto.addService = function(name, factory, order) {
    proto._services.push({
      key: name,
      item: factory,
      after: proto.get(order, 'after'),
      before: proto.get(order, 'before')
    });
  };

  // Exceptions
  proto.PermissionDenied = function(message) {
    this.detail = message;
    this.status = 403;

    this.toString = function() {
      return this.detail || 'Permission denied';
    };
  };
}());

(function (Misago) {
  'use strict';

  Misago.has = function(obj, key) {
    if (obj) {
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
      obj[key] = null;
    }
    return returnValue;
  };
}(Misago.prototype));

(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  Misago.input = function(kwargs) {
    var options = {
      disabled: kwargs.disabled || false,
      config: kwargs.config || persistent
    };

    if (kwargs.placeholder) {
      options.placeholder = kwargs.placeholder;
    }

    if (kwargs.autocomplete === false) {
      options.autocomplete = 'off';
    }

    var element = 'input';

    if (kwargs.id) {
      element += '#' + kwargs.id;
      options.key = 'field-' + kwargs.id;
    }

    element += '.form-control' + (kwargs.class || '');
    element += '[type="' + (kwargs.type || 'text') + '"]';

    if (kwargs.value) {
      options.value = kwargs.value();
      options.oninput = m.withAttr('value', kwargs.value);
    }

    return m(element, options);
  };
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var noop = function() {};

  Misago.stateHooks = function(component, loadingState, errorState) {
    /*
      Boilerplate for Misago components with lifecycles
    */

    // Component boilerplated (this may happen in tests)
    if (component._hasLifecycleHooks) {
      return component;
    }
    component._hasLifecycleHooks = true;

    // Component active state
    component.isActive = true;

    var errorHandler = errorState.bind(component);

    // Wrap controller to store lifecycle methods
    var _controller = component.controller || noop;
    component.controller = function() {
      try {
        component.isActive = true;
        var controller = _controller.apply(component, arguments) || {};

        // wrap onunload for lifestate
        var _onunload = controller.onunload || noop;
        controller.onunload = function() {
          _onunload.apply(component, arguments);
          component.isActive = false;
        };

        return controller;
      } catch (e) {
        errorHandler(e);
      }
    };

    // Add state callbacks to View-Model
    if (component.vm && component.vm.init) {
      // setup default loading view
      if (!component.loading) {
        var loadingHandler = loadingState.bind(component);
        component.loading = loadingHandler;
      }

      var _view = component.view;
      component.view = function() {
        if (component.vm.isReady) {
          return _view.apply(component, arguments);
        } else {
          return component.loading.apply(component, arguments);
        }
      };

      // wrap vm.init in promise handler
      var _init = component.vm.init;
      component.vm.init = function() {
        var initArgs = arguments;
        var promise = _init.apply(component.vm, initArgs);

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
              errorHandler(error);
            }
          });
        }
      };
    }

    return component;
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
  'use strict';

  Misago.Page = function(name, _) {
    var self = this;

    this.name = name;
    this.isFinalized = false;
    this._sections = [];

    var finalize = function() {
      if (!self.isFinalized) {
        self.isFinalized = true;

        var visible = [];
        self._sections.forEach(function (item) {
          if (!item.visibleIf || item.visibleIf(_)) {
            visible.push(item);
          }
        });
        self._sections = new Misago.OrderedList(visible).order(true);
      }
    };

    this.addSection = function(section) {
      if (this.isFinalized) {
        throw (this.name + " page was initialized already and no longer accepts new sections");
      }

      this._sections.push({
        key: section.link,
        item: section,

        after: section.after,
        before: section.before
      });
    };

    this.getSections = function() {
      finalize();
      return this._sections;
    };

    this.getDefaultLink = function() {
      finalize();
      return this._sections[0].link;
    };
  };
}(Misago.prototype));

(function (Misago) {
  Misago.serializeDatetime = function(serialized) {
    return serialized ? serialized.format() : null;
  };

  Misago.deserializeDatetime = function(deserialized) {
    return deserialized ? moment(deserialized) : null;
  };
}(Misago.prototype));

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
      if (pattern === '') {
        pattern = '/';
      }

      if (component instanceof Misago.UrlConf) {
        include(pattern, component.patterns());
      } else {
        this._patterns.push({
          pattern: pattern,
          component: component.replace(/_/g, '-'),
          name: name || component
        });
      }
    };
  };
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.loadingPage = function(_) {
    return m('.page.page-loading',
      _.component('loader')
    );
  };
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var getCsrfToken = function(cookie_name) {
    if (document.cookie.indexOf(cookie_name) !== -1) {
      var cookieRegex = new RegExp(cookie_name + '\=([^;]*)');
      var cookie = Misago.get(document.cookie.match(cookieRegex), 0);
      return cookie.split('=')[1];
    } else {
      return null;
    }
  };

  var Ajax = function(_) {
    this.refreshCsrfToken = function() {
      this.csrfToken = getCsrfToken(_.context.CSRF_COOKIE_NAME);
    };
    this.refreshCsrfToken();

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

        data: data || {},
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

    this.post = function(url, data) {
      return this.ajax('POST', url, data);
    };

    this.patch = function(url, data) {
      return this.ajax('PATCH', url, data);
    };

    this.put = function(url, data) {
      return this.ajax('PUT', url, data);
    };

    this.delete = function(url) {
      return this.ajax('DELETE', url);
    };
  };

  Misago.addService('ajax', function(_) {
    return new Ajax(_);
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var ALERT_BASE_DISPLAY_TIME = 5 * 1000;
  var ALERT_LENGTH_FACTOR = 70;
  var ALERT_MAX_DISPLAY_TIME = 9 * 1000;
  var ALERT_HIDE_ANIMATION_LENGTH = 300;

  var Alert = function(_) {
    var self = this;

    this.type = '';
    this.message = null;
    this.isVisible = false;

    var show = function(type, message) {
      self.type = type;
      self.message = message;
      self.isVisible = true;

      var displayTime = ALERT_BASE_DISPLAY_TIME;
      displayTime += message.length * ALERT_LENGTH_FACTOR;
      if (displayTime > ALERT_MAX_DISPLAY_TIME) {
        displayTime = ALERT_MAX_DISPLAY_TIME;
      }

      _.runloop.runOnce(function () {
        m.startComputation();
        self.isVisible = false;
        m.endComputation();
      }, 'flash-message-hide', displayTime);
    };

    var set = function(type, message) {
      _.runloop.stop('flash-message-hide');
      _.runloop.stop('flash-message-show');

      if (self.isVisible) {
        self.isVisible = false;
        _.runloop.runOnce(function () {
          m.startComputation();
          show(type, message);
          m.endComputation();
        }, 'flash-message-show', ALERT_HIDE_ANIMATION_LENGTH);
      } else {
        show(type, message);
      }
    };

    this.info = function(message) {
      set('info', message);
    };

    this.success = function(message) {
      set('success', message);
    };

    this.warning = function(message) {
      set('warning', message);
    };

    this.error = function(message) {
      set('error', message);
    };
  };

  Misago.addService('alert', {
    factory: function(_) {
      return new Alert(_);
    }
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var filtersUrl = function(filters) {
    if (typeof filters === 'object') {
      var values = [];
      for (var key in filters) {
        if (filters.hasOwnProperty(key)) {
          var encodedKey = encodeURIComponent(key);
          var encodedValue = encodeURIComponent(filters[key]);
          values.push(encodedKey + '=' + encodedValue);
        }
      }
      return '?' + values.join('&');
    } else {
      return filters + '/';
    }
  };

  var Query = function(_, call) {
    this.url = call.url || _.setup.api;

    if (call.path) {
      this.url += call.path + '/';
    } else if (call.related) {
      this.url += call.related + '/';
    } else {
      this.url += call.model + 's' + '/';
    }

    if (call.filters) {
      this.url += filtersUrl(call.filters);
    }

    if (call.model) {
      this.related = function(model, filters) {
        return new Query(_, {
          url: this.url,
          relation: call.model,
          related: model,
          filters: filters,
        });
      };
    }

    this.endpoint = function(path, filters) {
      return new Query(_, {
        url: this.url,
        path: path,
        filters: filters
      });
    };

    this.get = function() {
      var model = null;
      if (call.related) {
        model = call.relation + ':' + call.related;
      } else if (call.model) {
        model = call.model;
      }

      return _.ajax.get(this.url).then(function(data) {
        if (model) {
          if (data.results) {
            data.results.map(function(item) {
              return _.models.new(model, item);
            });
            return data;
          } else {
            return _.models.new(model, data);
          }
        } else {
          return data;
        }
      });
    };

    this.post = function(data) {
      return _.ajax.post(this.url, data);
    };

    this.patch = function(data) {
      return _.ajax.patch(this.url, data);
    };

    this.put = function(data) {
      return _.ajax.put(this.url, data);
    };

    this.delete = function() {
      return _.ajax.delete(this.url);
    };

    // shortcut for get()
    this.then = function(resolve, reject) {
      return this.get().then(resolve, reject);
    };
  };

  var Api = function(_) {
    this.model = function(model, filters) {
      return new Query(_, {
        model: model,
        filters: filters,
      });
    };

    this.endpoint = function(path, filters) {
      return new Query(_, {
        path: path,
        filters: filters
      });
    };

    this.alert = function(rejection) {
      // Shorthand for API errors
      var message = gettext("Unknown error has occured.");

      if (rejection.status === 0) {
        message = gettext("Lost connection with application.");
      }

      if (rejection.status === 403) {
        message = rejection.detail;
        if (message === "Permission denied") {
          message = gettext(
            "You don't have permission to perform this action.");
        }
      }

      if (rejection.status === 404) {
        message = gettext("Action link is invalid.");
      }

      _.alert.error(message);
    };
  };

  Misago.addService('api', function(_) {
    return new Api(_);
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var Auth = function(_) {
    var self = this;

    _.user = _.models.deserialize('user', _.context.user);

    // Auth state synchronization across tabs
    this.isDesynced = false; // becomes true if auth state between tabs differs
    this.newUser = null; // becomes user obj to which we want to sync

    var handleAuthChange = function(isAuthenticated) {
      if (!self.isDesynced) {
        m.startComputation();

        // display annoying "you were desynced" message
        self.isDesynced = true;

        if (isAuthenticated) {
          self.newUser = _.localstore.get('auth-user');
        }

        m.endComputation();
      }
    };

    var handleUserChange = function(newUser) {
      if (!self.isDesynced) {
        m.startComputation();

        if (_.user.id !== newUser.id) {
          self.isDesynced = true;
          self.newUser = newUser;
        } else if (newUser) {
          _.user = $.extend(_.user, newUser);
        }

        m.endComputation();
      }
    };

    var syncSession = function() {
      _.localstore.set('auth-user', _.user);
      _.localstore.set('auth-is-authenticated', _.user.isAuthenticated);

      _.localstore.watch('auth-is-authenticated', handleAuthChange);
      _.localstore.watch('auth-user', handleUserChange);
    };

    syncSession();

    // Access controls
    this.denyAuthenticated = function(message) {
      if (_.user.isAuthenticated) {
        throw new Misago.PermissionDenied(
          message || gettext("This page is not available to signed in users."));
      }
    };

    this.denyAnonymous = function(message) {
      if (_.user.isAnonymous) {
        throw new Misago.PermissionDenied(
          message || gettext("This page is not available to guests."));
      }
    };
  };

  Misago.addService('auth',
  function(_) {
    return new Auth(_);
  },
  {
    after: 'model:user'
  });
}(Misago.prototype));

/* global grecaptcha */
(function (Misago) {
  'use strict';

  var NoCaptcha = function() {
    var deferred = m.deferred();
    deferred.resolve();

    this.load = function() {
      return deferred.promise;
    };

    this.value = function() {
      return null;
    };
  };

  var QACaptcha = function(_) {
    var self = this;

    this.loading = false;
    this.question = null;
    this.value = m.prop('');

    var deferred = m.deferred();
    this.load = function() {
      this.value('');

      if (!this.question && !this.loading) {
        this.loading = true;

        _.api.endpoint('captcha-question').get().then(function(question) {
          self.question = question;
          deferred.resolve();
        }, function() {
          _.api.alert(gettext('Failed to load CAPTCHA.'));
          deferred.reject();
        }).then(function() {
          self.loading = true;
        });
      }

      return deferred.promise;
    };

    this.component = function(kwargs) {
      return _.component('form-group', {
        label: this.question.question,
        labelClass: kwargs.labelClass || null,
        controlClass: kwargs.controlClass || null,
        control: _.input({
          value: _.validate(kwargs.form, 'captcha'),
          id: 'id_captcha',
          disabled: kwargs.form.isBusy
        }),
        validation: kwargs.form.errors,
        validationKey: 'captcha',
        helpText: this.question.help_text
      });
    };

    this.validator = function() {
      return [];
    };
  };

  var ReCaptcha = function(_) {
    this.included = false;
    this.question = null;

    var deferred = m.deferred();

    var wait = function(promise) {
      if (typeof grecaptcha !== "undefined") {
        promise.resolve();
      } else {
        _.runloop.runOnce(function() {
          wait(promise);
        }, 'loading-grecaptcha', 150);
      }
    };

    this.load = function() {
      if (typeof grecaptcha !== "undefined") {
        grecaptcha.reset();
      }

      if (!this.included) {
        _.include('https://www.google.com/recaptcha/api.js', true);
        this.included = true;
      }

      wait(deferred);

      return deferred.promise;
    };

    var controlConfig = function(el, isInit, context) {
      context.retain = true;

      if (!isInit) {
        grecaptcha.render('recaptcha', {
          'sitekey': _.settings.recaptcha_site_key
        });
      }
    };

    this.component = function(kwargs) {
      var control = m('#recaptcha', {
        config: controlConfig
      });

      return _.component('form-group', {
        label: gettext("Security test"),
        labelClass: kwargs.labelClass || null,
        controlClass: kwargs.controlClass || null,
        control: control,
        validation: kwargs.form.errors,
        validationKey: 'captcha'
      });
    };

    this.value = function() {
      if (typeof grecaptcha !== "undefined") {
        return grecaptcha.getResponse();
      } else {
        return '';
      }
    };

    this.clean = function(form) {
      if (!this.value()) {
        form.errors.captcha = [
          gettext('This field is required.')
        ];
      } else {
        form.errors.captcha = true;
      }
    };

    this.validator = function() {
      return [];
    };
  };

  var Captcha = function(_) {
    var types = {
      'no': NoCaptcha,
      'qa': QACaptcha,
      're': ReCaptcha
    };

    var captcha = new types[_.settings.captcha_type](_);

    this.value = captcha.value;

    this.load = function() {
      return captcha.load();
    };

    this.component = function(kwargs) {
      if (captcha.component) {
        return captcha.component(kwargs);
      } else {
        return null;
      }
    };

    this.validator = function() {
      if (captcha.validator) {
        return captcha.validator();
      } else {
        return null;
      }
    };

    this.clean = function(form) {
      if (captcha.clean) {
        captcha.clean(form);
      } else {
        form.errors.captcha = true;
      }
    };
  };

  Misago.addService('captcha', function(_) {
    return new Captcha(_);
  },
  {
    after: 'include'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var component = function(name, component) {
    if (this._components[name]) {
      if (arguments.length > 1) {
        var argumentsArray = [this._components[name]];
        for (var i = 1; i < arguments.length; i += 1) {
          argumentsArray.push(arguments[i]);
        }
        argumentsArray.push(this);
        return m.component.apply(undefined, argumentsArray);
      } else {
        return m.component(this._components[name], this);
      }
    } else if (component) {
      this._components[name] = component;
    } else {
      throw '"' + name + '" component is not registered and can\'t be created';
    }
  };

  Misago.addService('components', function(_) {
    _._components = {};
    _.component = component;
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

  var Dropdown = function(_) {
    var slots = {};

    this.toggle = function(elementId, component) {
      var element = document.getElementById(elementId);

      if (element.hasChildNodes() && slots[elementId] === component) {
        slots[elementId] = null;
        m.mount(element, null);
        $(element).removeClass('open');
      } else {
        console.log(element.hasChildNodes());
        slots[elementId] = component;
        m.mount(element, _.component(component));
        $(element).addClass('open');
      }
    };

    this.destroy = function() {
      var element = null;

      for (var elementId in slots) {
        if (slots.hasOwnProperty(elementId)) {
          element = document.getElementById(elementId);
          if (element && element.hasChildNodes()) {
            m.mount(element, null);
          }
        }
      }
    };
  };

  Misago.addService('dropdown', {
    factory: function(_) {
      return new Dropdown(_);
    },
    destroy: function(_) {
      _.dropdown.destroy();
    }
  },
  {
    before: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var boilerplate = function(form) {
    var _submit = form.submit;
    var _success = form.success;
    var _error = form.error;

    form.isBusy = false;

    form.errors = null;

    form.submit = function() {
      if (form.isBusy) {
        return false;
      }

      if (form.clean) {
        if (form.clean()) {
          form.isBusy = true;
          _submit.apply(form);
        }
      } else {
        form.isBusy = true;
      }
      return false;
    };

    form.success = function() {
      m.startComputation();

      _success.apply(form, arguments);
      form.isBusy = false;

      m.endComputation();
    };

    form.error = function() {
      m.startComputation();

      _error.apply(form, arguments);
      form.isBusy = false;

      m.endComputation();
    };

    form.hasErrors = function() {
      if (form.errors === null) {
        return false;
      }

      for (var key in form.validation) {
        if (form.validation.hasOwnProperty(key)) {
          if (form.errors[key] !== true) {
            return true;
          }
        }
      }

      return false;
    };

    return form;
  };

  var form = function(name, constructor) {
    if (this._forms[name]) {
      if (constructor) {
        return boilerplate(new this._forms[name](constructor, this));
      } else {
        return boilerplate(new this._forms[name](this));
      }
    } else {
      this._forms[name] = constructor;
    }
  };

  Misago.addService('forms', function(_) {
    _._forms = {};
    _.form = form;
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var include = function(script, remote) {
    if (!remote) {
      script = this.context.STATIC_URL + script;
    }

    $.ajax({
      url: script,
      cache: true,
      dataType: 'script'
    });
  };

  Misago.addService('include', function(_) {
    _.include = include;
  },
  {
    after: 'conf'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var setLinks = function(_) {
    _.baseUrl = $('base').attr('href');

    var staticUrl = Misago.get(_.context, 'STATIC_URL', '/');
    var mediaUrl = Misago.get(_.context, 'MEDIA_URL', '/');

    // Media/Static urls
    var prefixUrl = function(prefix) {
      return function(url) {
        return prefix + url;
      };
    };

    _.staticUrl = prefixUrl(staticUrl);
    _.mediaUrl = prefixUrl(mediaUrl);
  };

  Misago.addService('links', function(_) {
    setLinks(_);
  });
}(Misago.prototype));

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

(function (Misago) {
  'use strict';

  var Modal = function() {
    var self = this;

    var element = document.getElementById('modal-mount');

    this.destroy = function() {
      $(element).off();
      $('body').removeClass('modal-open');
      $('.modal-backdrop').remove();
    };

    // Open/close modal
    var modal = $(element).modal({show: false});
    this.open = false;

    modal.on('hidden.bs.modal', function () {
      if (self.open) {
        m.mount(element, null);
        this.open = false;
      }
    });

    this.show = function(component) {
      this.open = true;
      m.mount(element, component);
      modal.modal('show');
    };

    this.hide = function() {
      modal.modal('hide');
    };
  };

  Misago.addService('_modal', {
    factory: function() {
      return new Modal();
    },
    destroy: function(_) {
      _._modal.destroy();
    }
  },
  {
    before: 'mount:page-component'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var modal = function(name, component) {
    if (this._modals[name]) {
      var argumentsArray = [this._modals[name]];
      for (var i = 1; i < arguments.length; i += 1) {
        argumentsArray.push(arguments[i]);
      }
      argumentsArray.push(this);
      this._modal.show(m.component.apply(m, argumentsArray));
    } else if (name) {
      this._modals[name] = component;
    } else {
      this._modal.hide();
    }
  };

  Misago.addService('modals', function(_) {
    _._modals = {};
    _.modal = modal;
  },
  {
    after: '_modal'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var Models = function() {
    this.classes = {};
    this.deserializers = {};

    this.add = function(name, kwargs) {
      if (kwargs.class) {
        this.classes[name] = kwargs.class;
      }

      if (kwargs.deserialize) {
        this.deserializers[name] = kwargs.deserialize;
      }
    };

    this.new = function(name, data) {
      if (this.classes[name]) {
        // Coerce ID to string
        // This is done to avoid type comparisions gotchas
        // later into app
        data.id = data.id ? String(data.id) : null;

        return new this.classes[name](data);
      } else {
        return data;
      }
    };

    this.deserialize = function(name, json) {
      if (this.deserializers[name]) {
        return this.new(name, this.deserializers[name](json, this));
      } else {
        return this.new(name, json);
      }
    };
  };

  Misago.addService('models', function() {
    return new Models();
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.addService('set-momentjs-locale', function() {
    moment.locale($('html').attr('lang'));
  });
}(Misago.prototype));

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

(function (Misago) {
  'use strict';

  var RunLoop = function(_) {
    var self = this;

    this._intervals = {};

    var stopInterval = function(name) {
      if (self._intervals[name]) {
        window.clearTimeout(self._intervals[name]);
        self._intervals[name] = null;
      }
    };

    this.run = function(callable, name, delay) {
      this._intervals[name] = window.setTimeout(function() {
        stopInterval(name);
        var result = callable(_);
        if (result !== false) {
          self.run(callable, name, delay);
        }
      }, delay);
    };

    this.runOnce = function(callable, name, delay) {
      this._intervals[name] = window.setTimeout(function() {
        stopInterval(name);
        callable(_);
      }, delay);
    };

    this.stop = function(name) {
      for (var loop in this._intervals) {
        if (!name || name === loop) {
          stopInterval(loop);
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

  Misago.addService('show-banned-page', function(_) {
    _.showBannedPage = function(ban, changeState) {
      var component = _.component(
        'banned-page', _.models.deserialize('ban', ban));

      if (typeof changeState === 'undefined' || !changeState) {
        _.title.set(gettext('You are banned'));
        window.history.pushState({}, "", _.context.BANNED_URL);
      }

      _.mountPage(component);
    };
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  Misago.addService('start-tick', function(_) {
    var ticks = m.prop();

    _.runloop.run(function() {
      m.startComputation();
      // just tick once a minute so stuff gets rerendered
      ticks(ticks() + 1);
      // syncing dynamic timestamps, etc ect
      m.endComputation();
    }, 'tick', 60000);
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var PageTitle = function(forum_name) {
    this.set = function(title) {
      if (title) {
        this._set_complex(title);
      } else {
        document.title = forum_name;
      }
    };

    this._set_complex = function(title) {
      if (typeof title === 'string') {
        title = {title: title};
      }

      var completeTitle = title.title;

      if (typeof title.page !== 'undefined' && title.page > 1) {
        var page_label = interpolate(
          gettext('page %(page)s'), { page:title.page }, true);
        completeTitle += ' (' + page_label + ')';
      }

      if (typeof title.parent !== 'undefined') {
        completeTitle += ' | ' + title.parent;
      }

      document.title = completeTitle + ' | ' + forum_name;
    };
  };

  Misago.addService('page-title', function(_) {
    _.title = new PageTitle(_.settings.forum_name);
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var EMAIL = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
  var USERNAME = new RegExp('^[0-9a-z]+$', 'i');

  // Validators namespace
  Misago.validators = {
    required: function() {
      return function(value) {
        if ($.trim(value).length === 0) {
          return gettext("This field is required.");
        }
      };
    },
    email: function(message) {
      return function(value) {
        if (!EMAIL.test(value)) {
          return message || gettext("Enter a valid email address.");
        }
      };
    },
    minLength: function(limit_value, message) {
      return function(value) {
        var returnMessage = '';
        var length = $.trim(value).length;

        if (length < limit_value) {
          if (message) {
            returnMessage = message(limit_value, length);
          } else {
            returnMessage = ngettext(
              "Ensure this value has at least %(limit_value)s character (it has %(show_value)s).",
              "Ensure this value has at least %(limit_value)s characters (it has %(show_value)s).",
              limit_value);
          }
          return interpolate(returnMessage, {
            limit_value: limit_value,
            show_value: length
          }, true);
        }
      };
    },
    maxLength: function(limit_value, message) {
      return function(value) {
        var returnMessage = '';
        var length = $.trim(value).length;

        if (length > limit_value) {
          if (message) {
            returnMessage = message(limit_value, length);
          } else {
            returnMessage = ngettext(
              "Ensure this value has at most %(limit_value)s character (it has %(show_value)s).",
              "Ensure this value has at most %(limit_value)s characters (it has %(show_value)s).",
              limit_value);
          }
          return interpolate(returnMessage, {
            limit_value: limit_value,
            show_value: length
          }, true);
        }
      };
    },
    usernameMinLength: function(settings) {
      var message = function(limit_value) {
        return ngettext(
          "Username must be at least %(limit_value)s character long.",
          "Username must be at least %(limit_value)s characters long.",
          limit_value);
      };
      return this.minLength(settings.username_length_min, message);
    },
    usernameMaxLength: function(settings) {
      var message = function(limit_value) {
        return ngettext(
          "Username cannot be longer than %(limit_value)s character.",
          "Username cannot be longer than %(limit_value)s characters.",
          limit_value);
      };
      return this.maxLength(settings.username_length_max, message);
    },
    usernameContent: function() {
      return function(value) {
        if (!USERNAME.test($.trim(value))) {
          return gettext("Username can only contain latin alphabet letters and digits.");
        }
      };
    },
    passwordMinLength: function(settings) {
      var message = function(limit_value) {
        return ngettext(
          "Valid password must be at least %(limit_value)s character long.",
          "Valid password must be at least %(limit_value)s characters long.",
          limit_value);
      };
      return this.minLength(settings.password_length_min, message);
    }
  };

  var validateField = function(value, validators) {
    var result = Misago.validators.required()(value);
    var errors = [];

    if (result) {
      return [result];
    } else {
      for (var i in validators) {
        result = validators[i](value);

        if (result) {
          errors.push(result);
        }
      }
    }

    return errors.length ? errors : true;
  };

  var validateForm = function(form) {
    var errors = {};
    var value = null;

    var isValid = true;

    for (var key in form.validation) {
      if (form.validation.hasOwnProperty(key)) {
        value = form[key]();
        errors[key] = validateField(form[key](), form.validation[key]);
        if (errors[key] !== true) {
          isValid = false;
        }
      }
    }

    form.errors = errors;
    return isValid;
  };

  var validate = function(form, name) {
    if (name) {
      return function(value) {
        var errors = null;
        if (typeof value !== 'undefined') {
          errors = validateField(value, form.validation[name]);
          if (errors) {
            if (!form.errors) {
              form.errors = {};
            }
            form.errors[name] = errors;
          }
          form[name](value);
          return form[name](value);
        } else {
          return form[name]();
        }
      };
    } else {
      return validateForm(form);
    }
  };

  Misago.addService('validate', {
    factory: function() {
      return validate;
    }
  });
}(Misago.prototype));

/* global zxcvbn */
(function (Misago) {
  'use strict';

  var Zxcvbn = function(_) {
    this.included = false;

    this.scorePassword = function(password, inputs) {
      // 0-4 score, the more the stronger password
      return zxcvbn(password, inputs).score;
    };

    // loading
    this.include = function() {
      _.include('misago/js/zxcvbn.js');
      this.included = true;
    };

    var wait = function(promise) {
      if (typeof zxcvbn !== "undefined") {
        promise.resolve();
      } else {
        _.runloop.runOnce(function() {
          wait(promise);
        }, 'loading-zxcvbn', 150);
      }
    };

    var deferred = m.deferred();
    this.load = function() {
      if (!this.included) {
        this.include();
      }
      wait(deferred);
      return deferred.promise;
    };
  };

  Misago.addService('zxcvbn', function(_) {
    return new Zxcvbn(_);
  },
  {
    after: 'include'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var Ban = function(data) {
    this.message = {
      html: data.message.html,
      plain: data.message.plain,
    };

    this.expires_on = data.expires_on;
  };

  var deserializeBan = function(data) {
    data.expires_on = Misago.deserializeDatetime(data.expires_on);

    return data;
  };

  Misago.addService('model:ban', function(_) {
    _.models.add('ban', {
      class: Ban,
      deserialize: deserializeBan
    });
  },
  {
    after: 'models'
  });
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var LegalPage = function(data) {
    this.title = data.title;
    this.body = data.body;
    this.link = data.link;
  };

  Misago.addService('model:legal-page', function(_) {
    _.models.add('legal-page', {
      class: LegalPage
    });
  },
  {
    after: 'models'
  });
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var Rank = function(data) {
    this.id = data.id;

    this.name = data.name;
    this.slug = data.slug;

    this.description = data.description;

    this.title = data.title;
    this.css_class = data.css_class;

    this.is_tab = data.is_tab;
  };

  Misago.addService('model:rank', function(_) {
    _.models.add('rank', {
      class: Rank
    });
  },
  {
    after: 'models'
  });
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var User = function(data) {
    this.id = data.id;

    this.isAuthenticated = !!this.id;
    this.isAnonymous = !this.isAuthenticated;

    this.username = data.username;
    this.slug = data.slug;

    this.email = data.email;

    this.full_title = data.full_title;
    this.rank = data.rank;

    this.avatar_hash = data.avatar_hash;

    this.acl = data.acl;

    this.absolute_url = data.absolute_url;
  };

  var deserializeUser = function(data, models) {
    if (data.joined_on) {
      data.joined_on = Misago.deserializeDatetime(data.joined_on);
    }

    if (data.rank) {
      data.rank = models.deserialize('rank', data.rank);
    }

    return data;
  };

  Misago.addService('model:user', function(_) {
    _.models.add('user', {
      class: User,
      deserialize: deserializeUser
    });
  },
  {
    after: 'model:rank'
  });
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var style = '.well.well-form.well-form-request-activation-link';

  var ViewModel = function(api) {
    this.api = api;
    this.user = null;

    this.success = function(user) {
      this.user = user;
    };

    this.error = function(rejection, _) {
      if (rejection.code === 'already_active') {
        _.alert.info(rejection.detail);
        _.modal('sign-in');
      } else if (rejection.code === 'inactive_admin') {
        _.alert.info(rejection.detail);
      } else {
        _.alert.error(rejection.detail);
      }
    };

    this.reset = function() {
      this.user = null;
    };
  };

  var form = {
    controller: function(_) {
      var vm = new ViewModel(_.context.SEND_ACTIVATION_API_URL);

      return {
        vm: vm,
        form: _.form('request-link', vm)
      };
    },
    view: function(ctrl, _) {
      if (ctrl.vm.user) {
        return this.done(ctrl.vm, ctrl.form, _);
      } else {
        return this.form(ctrl.form, _);
      }
    },
    done: function(vm, form, _) {
      var message = gettext("Activation link sent to %(email)s.");

      return m(style + '.well-done',
        m('.done-message', [
          m('.message-icon',
            m('span.material-icon', 'check')
          ),
          m('.message-body',
            m('p',
              interpolate(message, {
                email: vm.user.email
              }, true)
            )
          ),
          _.component('button', {
            class: '.btn-default.btn-block',
            submit: false,
            label: gettext("Request another link"),
            onclick: form.reset.bind(form)
          })

        ])
      );
    },
    form: function(form, _) {
      return m(style,
        m('form', {onsubmit: form.submit}, [
          m('.form-group',
            m('.control-input',
              Misago.input({
                disabled: form.isBusy,
                value: form.email,
                placeholder: gettext("Your e-mail address")
              })
            )
          ),
          _.component('button', {
            class: '.btn-primary.btn-block',
            submit: true,
            loading: form.isBusy,
            label: gettext("Send link")
          })
        ])
      );
    }
  };

  Misago.addService('component:request-link-form', function(_) {
    _.component('request-activation-link-form', form);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var header = {
    view: function(ctrl, title) {
      return m('.modal-header', [
        m('button.close[type="button"]',
          {'data-dismiss': 'modal', 'aria-label': gettext('Close')},
          m('span', {'aria-hidden': 'true'}, m.trust('&times;'))
        ),
        m('h4#misago-modal-label.modal-title', title)
      ]);
    }
  };

  Misago.addService('component:modal:header', function(_) {
    _.component('modal:header', header);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  var refresh = function() {
    document.location.reload();
  };

  var registerComplete = {
    controller: function(message, _) {
      if (message.activation === 'active') {
        _.runloop.runOnce(
          refresh, 'refresh-after-registration', 10000);
      }
    },
    view: function(ctrl, message, _) {
      var messageHtml = null;

      if (message.activation === 'active') {
        messageHtml = this.active(message);
      } else {
        messageHtml = this.inactive(message);
      }

      return m('.modal-dialog.modal-message.modal-register[role="document"]',
        {config: persistent},
        m('.modal-content', [
          _.component('modal:header', gettext('Registration complete')),
          m('.modal-body',
            messageHtml
          )
        ])
      );
    },
    active: function(message) {
      var lead = gettext("%(username)s, your account has been created and you were signed in.");
      return [
        m('.message-icon',
          m('span.material-icon', 'check')
        ),
        m('.message-body', [
          m('p.lead',
            interpolate(lead, {'username': message.username}, true)
          ),
          m('p',
            gettext('The page will refresh automatically in 10 seconds.')
          ),
          m('p',
            m('button[type="button"].btn.btn-default', {onclick: refresh},
              gettext('Refresh page')
            )
          )
        ])
      ];
    },
    inactive: function(message) {
      var lead = null;
      var help = null;

      if (message.activation === 'user') {
        lead = gettext("%(username)s, your account has been created but you need to activate it before you will be able to sign in.");
        help = gettext("We have sent an e-mail to %(email)s with link that you have to click to activate your account.");
      } else if (message.activation === 'admin') {
        lead = gettext("%(username)s, your account has been created but board administrator will have to activate it before you will be able to sign in.");
        help = gettext("We will send an e-mail to %(email)s when this takes place.");
      }

      return [
        m('.message-icon',
          m('span.material-icon', 'info_outline')
        ),
        m('.message-body', [
          m('p.lead',
            interpolate(lead, {'username': message.username}, true)
          ),
          m('p',
            interpolate(help, {'email': message.email}, true)
          )
        ])
      ];
    }
  };

  Misago.addService('modal:register-complete', function(_) {
    _.modal('register-complete', registerComplete);
  },
  {
    after: 'modals'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  var register = {
    controller: function(_) {
      return {
        form: _.form('register')
      };
    },
    view: function(ctrl, _) {
      var captcha = _.captcha.component({
        form: ctrl.form,

        labelClass: '.col-md-4',
        controlClass: '.col-md-8'
      });

      var footnote = null;

      if (_.context.TERMS_OF_SERVICE_URL) {
        footnote = m('a', {href: _.context.TERMS_OF_SERVICE_URL},
          m.trust(interpolate(gettext("By registering you agree to site's %(terms)s."), {
            terms: '<strong>' + gettext("terms and conditions") + '</strong>'
          }, true))
        );
      }

      return m('.modal-dialog.modal-form.modal-register[role="document"]',
        {config: persistent},
        m('.modal-content', [
          _.component('modal:header', gettext('Register')),
          m('form.form-horizontal',
          {
            onsubmit: ctrl.form.submit
          },
          [
            m('input[type="text"]', {
              name:'_username',
              style: 'display: none'
            }),
            m('input[type="password"]', {
              name:'_password',
              style: 'display: none'
            }),
            m('.modal-body', [
              _.component('form-group', {
                label: gettext("Username"),
                labelClass: '.col-md-4',
                controlClass: '.col-md-8',
                control: _.input({
                  value: _.validate(ctrl.form, 'username'),
                  id: 'id_username',
                  disabled: ctrl.form.isBusy
                }),
                validation: ctrl.form.errors,
                validationKey: 'username'
              }),
              _.component('form-group', {
                label: gettext("E-mail"),
                labelClass: '.col-md-4',
                controlClass: '.col-md-8',
                control: _.input({
                  value: _.validate(ctrl.form, 'email'),
                  id: 'id_email',
                  disabled: ctrl.form.isBusy
                }),
                validation: ctrl.form.errors,
                validationKey: 'email'
              }),
              _.component('form-group', {
                label: gettext("Password"),
                labelClass: '.col-md-4',
                controlClass: '.col-md-8',
                control: _.input({
                  value: _.validate(ctrl.form, 'password'),
                  type: 'password',
                  id: 'id_password',
                  disabled: ctrl.form.isBusy
                }),
                validation: ctrl.form.errors,
                validationKey: 'password',
                helpText: _.component('password-strength', {
                  inputs: [
                    ctrl.form.username(),
                    ctrl.form.email()
                  ],
                  password: ctrl.form.password()
                })
              }),
              captcha
            ]),
            m('.modal-footer', [
              footnote,
              _.component('button', {
                class: '.btn-primary',
                submit: true,
                loading: ctrl.form.isBusy,
                label: gettext("Register account")
              })
            ])
          ])
        ])
      );
    }
  };

  Misago.addService('modal:register', function(_) {
    _.modal('register', register);
  },
  {
    after: 'modals'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  var signin = {
    controller: function(_) {
      return {
        form: _.form('sign-in')
      };
    },
    view: function(ctrl, _) {
      var activateButton = null;

      if (ctrl.form.showActivation) {
        activateButton = m('a.btn.btn-block.btn-success',
          {href: _.context.REQUEST_ACTIVATION_URL},
          gettext("Activate account")
        );
      }

      return m('.modal-dialog.modal-sm.modal-signin[role="document"]',
        {config: persistent},
        m('.modal-content', [
          _.component('modal:header', gettext("Sign in")),
          m('form', {onsubmit: ctrl.form.submit}, [
            m('.modal-body', [
              m('.form-group',
                m('.control-input',
                  Misago.input({
                    disabled: ctrl.form.isBusy,
                    value: ctrl.form.username,
                    placeholder: gettext("Username or e-mail")
                  })
                )
              ),
              m('.form-group',
                m('.control-input',
                  Misago.input({
                    type: 'password',
                    disabled: ctrl.form.isBusy,
                    value: ctrl.form.password,
                    placeholder: gettext("Password")
                  })
                )
              )
            ]),
            m('.modal-footer', [
              activateButton,
              _.component('button', {
                class: '.btn-primary.btn-block',
                submit: true,
                loading: ctrl.form.isBusy,
                label: gettext("Sign in")
              }),
              m('a.btn.btn-block.btn-default',
                {href: _.context.FORGOTTEN_PASSWORD_URL},
                gettext("Forgot password?")
              )
            ])
          ])
        ])
      );
    }
  };

  Misago.addService('modal:sign-in', function(_) {
    _.modal('sign-in', signin);
  },
  {
    after: 'modals'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var dropdown = {
    controller: function(_) {
      return {
        showSignIn: function() {
          _.modal('sign-in');
        }
      };
    },
    view: function(ctrl, _) {
      return m('ul.dropdown-menu.user-dropdown.dropdown-menu-right[role="menu"]',
        m('li.guest-preview', [
          m('h4',
            gettext("You are browsing as guest.")
          ),
          m('p',
            gettext('Sign in or register to start and participate in discussions.')
          ),
          m('.row', [
            m('.col-xs-6',
              _.component('button', {
                class: '.btn.btn-default.btn-block',
                onclick: ctrl.showSignIn,
                disabled: ctrl.isBusy,
                label: gettext('Sign in')
              })
            ),
            m('.col-xs-6',
              _.component(
                'navbar:register-button', '.btn.btn-primary.btn-block')
            )
          ])
        ])
      );
    }
  };

  Misago.addService('component:navbar:dropdown:guest', function(_) {
    _.component('navbar:dropdown:guest', dropdown);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var navbar = {
    style: '.nav.navbar-nav.navbar-compact-nav.hidden-md.hidden-lg',
    controller: function(links, _) {
      return {
        openUserMenu: function() {
          if (_.user.isAuthenticated) {
            _.dropdown.toggle('navbar-dropdown', 'navbar:dropdown:user');
          } else {
            _.dropdown.toggle('navbar-dropdown', 'navbar:dropdown:guest');
          }

          return false;
        }
      };
    },
    userMenu: function(ctrl, _) {
      if (_.user.isAuthenticated) {
        return {
          element: _.component('user-avatar', _.user, 64),
          config: {
            onclick: ctrl.openUserMenu,
            url: '/not-yet/',

            'data-misago-routed': 'false'
          }
        };
      } else {
        return {
          element: _.component('user-avatar', null, 64),
          config: {
            onclick: ctrl.openUserMenu,
            href: '#',

            'data-misago-routed': 'false'
          }
        };
      }
    },
    mobileNav: function(ctrl, links, _) {
      var mobileLinks = [
        {
          element: m('img', {
            src: _.router.staticUrl('misago/img/site-icon.png'),
            alt: _.settings.forum_name
          }),
          url: _.router.url('index')
        }
      ];

      links.forEach(function(link) {
        if (link.url !== mobileLinks[0].url) {
          mobileLinks.push(link);
        }
      });

      mobileLinks.push(this.userMenu(ctrl, _));

      return mobileLinks;
    },
    view: function(ctrl, links, _) {
      var mobileLinks = this.mobileNav(ctrl, links, _);

      return m('ul' + this.style + '.with-' + mobileLinks.length + '-items',
        mobileLinks.map(function(link) {
          return m('li',
            m('a', link.config || {href: link.url},
              link.element || m('span.material-icon', {title:link.label},
                link.icon
              )
            )
          );
        })
      );
    }
  };

  Misago.addService('component:navbar:mobile', function(_) {
    _.component('navbar:mobile', navbar);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var button = {
    controller: function(style, _) {
      return {
        isBusy: false,

        showRegister: function() {
          if (_.settings.account_activation === 'closed') {
            _.alert.info(gettext("New registrations are currently disabled."));
          } else {
            m.startComputation();
            this.isBusy = true;
            m.endComputation();

            var self = this;
            m.sync([
              _.zxcvbn.load(),
              _.captcha.load()
            ]).then(function() {
              _.modal('register');
            }, function() {
              _.alert.error(gettext('Registation is not available now due to an error.'));
            }).then(function() {
              m.startComputation();
              self.isBusy = false;
              m.endComputation();
            });
          }
        }
      };
    },
    view: function(ctrl, style, _) {
      return _.component('button', {
        class: style,
        onclick: ctrl.showRegister.bind(ctrl),
        loading: ctrl.isBusy,
        label: gettext('Register')
      });
    }
  };

  Misago.addService('component:navbar:register-button', function(_) {
    _.component('navbar:register-button', button);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var dropdown = {
    class: '.dropdown-menu.user-dropdown.dropdown-menu-right',

    controller: function() {
      return {
        logout: function() {
          var decision = confirm(gettext("Are you sure you want to sign out?"));
          if (decision) {
            $('#hidden-logout-form').submit();
          }
        }
      };
    },
    view: function(ctrl, _) {
      return m('ul' + this.class + '[role="menu"]', [
        m('li.dropdown-header',
          m('strong',
            _.user.username
          )
        ),
        m('li.divider'),
        m('li',
          m('a', {href: _.user.absolute_url}, [
            m('span.material-icon',
              'account_circle'
            ),
            gettext("See your profile")
          ])
        ),
        m('li',
          m('a', {href: _.context.USERCP_URL}, [
            m('span.material-icon',
              'done_all'
            ),
            gettext("Change options")
          ])
        ),
        m('li',
          m('button.btn-link[type="button"]', [
            m('span.material-icon',
              'face'
            ),
            gettext("Change avatar")
          ])
        ),
        m('li.divider'),
        m('li.dropdown-footer',
          m('button.btn.btn-default.btn-block', {onclick: ctrl.logout},
            gettext("Logout")
          )
        )
      ]);
    }
  };

  Misago.addService('component:navbar:dropdown:user', function(_) {
    _.component('navbar:dropdown:user', dropdown);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var nav = {
    controller: function(_) {
      return {
        openUserMenu: function() {
          _.dropdown.toggle('navbar-dropdown', 'navbar:dropdown:guest');
        }
      };
    },
    view: function(ctrl, _) {
      return m('button', {type: 'button', onclick: ctrl.openUserMenu},
        _.component('user-avatar', null, 64)
      );
    }
  };

  Misago.addService('component:navbar:compact:guest-nav', function(_) {
    _.component('navbar:compact:guest-nav', nav);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var nav = {
    controller: function(_) {
      return {
        openUserMenu: function() {
          _.dropdown.toggle('navbar-dropdown', 'navbar:dropdown:user');
          return false;
        }
      };
    },
    view: function(ctrl, _) {
      var config = {
        onclick: ctrl.openUserMenu,
        href: _.user.absolute_url
      };

      return m('a', config,
        _.component('user-avatar', _.user, 64)
      );
    }
  };

  Misago.addService('component:navbar:compact:user-nav', function(_) {
    _.component('navbar:compact:user-nav', nav);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var nav = {
    controller: function(_) {
      return {
        showSignIn: function() {
          _.modal('sign-in');
        }
      };
    },
    view: function(ctrl, _) {
      return m('div.nav.nav-guest', [
        _.component('button', {
          class: '.navbar-btn.btn-default',
          onclick: ctrl.showSignIn,
          disabled: ctrl.isBusy,
          label: gettext('Sign in')
        }),
        _.component('navbar:register-button', '.navbar-btn.btn-primary')
      ]);
    }
  };

  Misago.addService('component:navbar:desktop:guest-nav', function(_) {
    _.component('navbar:desktop:guest-nav', nav);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var nav = {
    controller: function(_) {
      return {
        dropdownToggle: {
          href: _.user.absolute_url,

          'data-toggle': 'dropdown',
          'data-misago-routed': 'false',

          'aria-haspopup': 'true',
          'aria-expanded': 'false'
        }
      };
    },
    view: function(ctrl, _) {
      return m('ul.nav.navbar-nav.nav-user', [
        m('li.dropdown', [
          m('a.dropdown-toggle[role="button"]', ctrl.dropdownToggle,
            _.component('user-avatar', _.user, 64)
          ),
          _.component('navbar:dropdown:user')
        ])
      ]);
    }
  };

  Misago.addService('component:navbar:desktop:user-nav', function(_) {
    _.component('navbar:desktop:user-nav', nav);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  var alert = {
    classes: {
      'info': 'alert-info',
      'success': 'alert-success',
      'warning': 'alert-warning',
      'error': 'alert-danger'
    },
    view: function(ctrl, _) {
      var config = {
        config: persistent,
        class: _.alert.isVisible ? 'in' : 'out'
      };

      return m('.alerts', config,
        m('p.alert', {class: this.classes[_.alert.type]},
          _.alert.message
        )
      );
    }
  };

  Misago.addService('component:alert', function(_) {
    _.component('alert', alert);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  var authChanged = {
    refresh: function() {
      window.location.reload();
    },
    view: function(ctrl, _) {
      var message = '';

      var options = {
        config: persistent,
        class: (_.auth.isDesynced ? 'show' : null)
      };

      if (_.auth.isDesynced) {
        if (_.auth.newUser && _.auth.newUser.isAuthenticated) {
          message = gettext("You have signed in as %(username)s. Please refresh this page before continuing.");
          message = interpolate(message, {username: _.auth.newUser.username}, true);
        } else {
          message = gettext("%(username)s, you have been signed out. Please refresh this page before continuing.");
          message = interpolate(message, {username: _.user.username}, true);
        }
      }

      return m('.auth-changed-message', options,
        m('',
          m('.container', [
            m('p',
              message
            ),
            m('p', [
              m('button.btn.btn-default[type="button"]', {onclick: this.refresh},
                gettext("Reload page")
              ),
              m('span.hidden-xs.hidden-sm.text-muted',
                gettext("or press F5 key.")
              )
            ])
          ])
        )
      );
    }
  };

  Misago.addService('component:auth-changed-message', function(_) {
    _.component('auth-changed-message', authChanged);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var banExpirationMessage = {
    controller: function(ban, container) {
      var _ = container || ban;

      if (container) {
        return ban;
      } else {
        return _.models.deserialize('ban', _.context.ban);
      }
    },
    view: function(ban) {
      var expirationMessage = null;
      if (ban.expires_on) {
        if (ban.expires_on.isAfter(moment())) {
          expirationMessage = interpolate(
            gettext('This ban expires %(expires_on)s.'),
            {'expires_on': ban.expires_on.fromNow()},
            true);
        } else {
          expirationMessage = gettext('This ban has expired.');
        }
      } else {
        expirationMessage = gettext('This ban is permanent.');
      }

      return m('p', expirationMessage);
    }
  };

  Misago.addService('component:ban-expiration-message', function(_) {
    _.component('ban-expiration-message', banExpirationMessage);
  },
  {
    after: 'components'
  });
}(Misago.prototype));


(function (Misago) {
  'use strict';

  var bannedPage = {
    view: function(ctrl, ban, _) {
      var error_message = [];

      if (ban.message.html) {
        error_message.push(m('.lead', m.trust(ban.message.html)));
      } else {
        error_message.push(m('p.lead', ban.message.plain));
      }

      error_message.push(_.component('ban-expiration-message', ban));

      return m('.page.page-error.page-error-banned',
        m('.container',
          m('.message-panel', [
            m('.message-icon',
              m('span.material-icon', 'highlight_off')
            ),
            m('.message-body', error_message)
          ])
        )
      );
    }
  };

  Misago.addService('component:banned-page', function(_) {
    _.component('banned-page', bannedPage);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var button = {
    view: function(ctrl, kwargs) {
      var options = {
        disabled: kwargs.disabled || kwargs.loading || false,
        config: kwargs.config || null,
        loading: kwargs.loading || false,
        type: kwargs.submit ? 'submit' : 'button',
        onclick: kwargs.onclick || null
      };

      var element = 'button[type="' + options.type + '"].btn';
      if (options.loading) {
        element += '.btn-loading';
      }

      if (kwargs.id) {
        element += '#' + kwargs.id;
      }

      element += (kwargs.class || '');

      var label = kwargs.label;
      if (options.loading) {
        label = [
          label,
          m('.loader-compact', [
            m('.bounce1'),
            m('.bounce2'),
            m('.bounce3')
          ])
        ];
      }

      return m(element, options, label);
    },
  };

  Misago.addService('component:button', function(_) {
    _.component('button', button);
  },
  {
    after: 'components'
  });
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var textFields = ['text', 'password', 'email'];

  var formGroup = {
    view: function(ctrl, kwargs) {
      var groupClass = '.form-group';
      var errors = null;
      var helpText = null;

      var controlType = kwargs.control.attrs.type;
      var controlId = kwargs.control.attrs.id;

      var feedbackId = controlId + '_feedback';
      var feedbackIcon = null;
      var showFeedbackIcon = null;

      var isValidated = kwargs.validationKey && kwargs.validation !== null;

      kwargs.control.attrs['aria-describedby'] = '';

      if (isValidated && kwargs.validation[kwargs.validationKey]) {
        showFeedbackIcon = textFields.indexOf(controlType) >= 0;
        kwargs.control.attrs['aria-describedby'] = feedbackId;

        if (kwargs.validation[kwargs.validationKey] === true) {
          groupClass += '.has-success';
          feedbackIcon = [
            m('span.material-icon.form-control-feedback',
              {
                'aria-hidden': 'true'
              },
              'check'
            ),
            m('span.sr-only#' + feedbackId, gettext("(success)"))
          ];
        } else {
          groupClass += '.has-error';
          errors = kwargs.validation[kwargs.validationKey];
          feedbackIcon = [
            m('span.material-icon.form-control-feedback',
              {
                'aria-hidden': 'true'
              },
              'clear'
            ),
            m('span.sr-only#' + feedbackId, gettext("(error)"))
          ];
        }
      }

      if (kwargs.helpText) {
        if (typeof kwargs.helpText === 'string' ||
            kwargs.helpText instanceof String) {
          helpText = m('p.help-block', kwargs.helpText);
        } else {
          helpText = kwargs.helpText;
        }
      }

      return m(groupClass, [
        m('label.control-label' + (kwargs.labelClass || ''),
          {
            for: kwargs.labelFor || controlId
          },
          kwargs.label + ':'
        ),
        m(kwargs.controlClass || '', [
          kwargs.control,
          showFeedbackIcon ? feedbackIcon : null,
          errors ? m('.help-block.errors', errors.map(function(item) {
            return m('p', item);
          })) : null,
          helpText
        ])
      ]);
    },
  };

  Misago.addService('component:form-group', function(_) {
    _.component('form-group', formGroup);
  },
  {
    after: 'components'
  });
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var loader = {
    view: function() {
      return m('.loader.sk-folding-cube', [
        m('.sk-cube1.sk-cube'),
        m('.sk-cube2.sk-cube'),
        m('.sk-cube4.sk-cube'),
        m('.sk-cube3.sk-cube')
      ]);
    }
  };

  Misago.addService('component:loader', function(_) {
    _.component('loader', loader);
  },
  {
    after: 'components'
  });
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  var markup = {
    view: function(ctrl, content) {
      return m('article.misago-markup', {config: persistent},
        m.trust(content)
      );
    }
  };

  Misago.addService('component:markup', function(_) {
    _.component('markup', markup);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var header = {
    view: function(ctrl, options) {
      return m('.page-header',
        m('.container', [
          m('h1', options.title),
        ])
      );
    }
  };

  Misago.addService('component:header', function(_) {
    _.component('header', header);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  var styles = [
    'progress-bar-danger',
    'progress-bar-warning',
    'progress-bar-warning',
    'progress-bar-primary',
    'progress-bar-success'
  ];

  var labels = [
    gettext('Entered password is very weak.'),
    gettext('Entered password is weak.'),
    gettext('Entered password is average.'),
    gettext('Entered password is strong.'),
    gettext('Entered password is very strong.')
  ];

  var passwordStrength = {
    view: function(ctrl, kwargs, _) {
      var score = _.zxcvbn.scorePassword(kwargs.password, kwargs.inputs);
      var options = {
        config: persistent,
        class: styles[score],
        style: "width: " + (20 + (20 * score)) + '%',
        'role': "progressbar",
        'aria-valuenow': score,
        'aria-valuemin': "0",
        'aria-valuemax': "4"
      };

      return m('.help-block.password-strength', {key: 'password-strength'}, [
        m('.progress',
          m('.progress-bar', options,
            m('span.sr-only', labels[score])
          )
        ),
        m('p.text-small', labels[score])
      ]);
    },
  };

  Misago.addService('component:password-strength', function(_) {
    _.component('password-strength', passwordStrength);
  },
  {
    after: 'components'
  });
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var avatar = {
    defaultSize: 100,

    src: function(user, size, _) {
      var src = _.baseUrl + 'user-avatar/';

      if (user && user.id) {
        // just avatar hash, size and user id
        src += user.avatar_hash + '/' + size + '/' + user.id + '.png';
      } else {
        // just append avatar size to file to produce no-avatar placeholder
        src += size + '.png';
      }

      return src;
    },
    view: function(ctrl, user, size, _) {
      var finalSize = size || this.defaultSize;
      return m('img', {
        alt: user && user.username ? user.username : gettext("Unregistered"),
        width: finalSize,
        height: finalSize,
        src: this.src(user, finalSize, _)
      });
    }
  };

  Misago.addService('component:user-avatar', function(_) {
    _.component('user-avatar', avatar);
  },
  {
    after: 'components'
  });
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var ChangePassword = function(_) {
    var self = this;

    this.username = null;
    this.password = m.prop('');

    this.validation = {
      'password': [
        Misago.validators.passwordMinLength(_.settings)
      ]
    };

    this.clean = function() {
      if (!_.validate(this)) {
        if ($.trim(this.password()).length) {
          _.alert.error(this.errors.password);
        } else {
          _.alert.error(gettext("Enter new password."));
        }
        return false;
      } else {
        return true;
      }
    };

    this.submit = function() {
      var endpoint = _.api.endpoint('auth').endpoint('change-password');
      endpoint = endpoint.endpoint(m.route.param('user_id'));
      endpoint = endpoint.endpoint(m.route.param('token'));

      endpoint.post({
        password: self.password()
      }).then(function(user) {
        self.success(user);
      }, function(error) {
        self.error(error);
      });
    };

    this.success = function(user) {
      this.username = user.username;
    };

    this.error = function(rejection) {
      if (rejection.status === 403 && rejection.ban) {
        _.router.error403({
          message: '',
          ban: rejection.ban
        });
      } else if (rejection.status === 400) {
        _.alert.error(rejection.detail);
      } else {
        _.api.alert(rejection);
      }
    };
  };

  Misago.addService('form:change-password', function(_) {
    _.form('change-password', ChangePassword);
  },
  {
    after: 'forms'
  });
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var Register = function(_) {
    var self = this;

    this.showActivation = false;

    this.username = m.prop('');
    this.email = m.prop('');
    this.password = m.prop('');

    this.captcha = _.captcha.value;

    this.errors = null;

    this.validation = {
      'username': [
        Misago.validators.usernameContent(),
        Misago.validators.usernameMinLength(_.settings),
        Misago.validators.usernameMaxLength(_.settings)
      ],
      'email': [
        Misago.validators.email()
      ],
      'password': [
        Misago.validators.passwordMinLength(_.settings)
      ],
      'captcha': _.captcha.validator()
    };

    this.clean = function() {
      if (this.errors === null) {
        _.validate(this);
      }

      _.captcha.clean(this);

      if (this.hasErrors()) {
        _.alert.error(gettext("Form contains errors."));
        return false;
      } else {
        return true;
      }
    };

    this.submit = function() {
      _.api.model('user').post({
        username: this.username(),
        email: this.email(),
        password: this.password(),
        captcha: this.captcha()
      }).then(this.success, this.error);
    };

    this.success = function(data) {
      _.modal('register-complete', data);
    };

    this.error = function(rejection) {
      if (rejection.status === 400) {
        _.alert.error(gettext("Form contains errors."));
        $.extend(self.errors, rejection);
      } else {
        _.api.alert(rejection);
      }
    };
  };

  Misago.addService('form:register', function(_) {
    _.form('register', Register);
  },
  {
    after: 'forms'
  });
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var RequestLink = function(vm, _) {
    var self = this;

    this.email = m.prop('');

    this.validation = {
      'email': [
        Misago.validators.email()
      ]
    };

    this.clean = function() {
      if (!_.validate(this)) {
        _.alert.error(gettext("Enter a valid email address."));
        return false;
      } else {
        return true;
      }
    };

    this.submit = function() {
      _.ajax.post(vm.api, {
        email: self.email()
      }).then(function(user) {
        self.success(user);
      }, function(error) {
        self.error(error);
      });
    };

    this.success = function(user) {
      vm.success(user);
    };

    this.error = function(rejection) {
      if (rejection.status === 400) {
          vm.error(rejection, _);
      } else {
        _.api.alert(rejection);
      }
    };

    this.reset = function() {
      this.email('');
      vm.reset();
    };
  };

  Misago.addService('form:request-link', function(_) {
    _.form('request-link', RequestLink);
  },
  {
    after: 'forms'
  });
} (Misago.prototype));

(function (Misago) {
  'use strict';

  var SignIn = function(_) {
    var self = this;

    this.showActivation = false;

    this.username = m.prop('');
    this.password = m.prop('');

    this.validation = {
      'username': [],
      'password': []
    };

    this.clean = function() {
      if (!_.validate(this)) {
        _.alert.error(gettext("Fill out both fields."));
        return false;
      } else {
        return true;
      }
    };

    this.submit = function() {
      _.api.endpoint('auth').post({
        username: self.username(),
        password: self.password()
      }).then(function() {
        self.success();
      }, function(error) {
        self.error(error);
      });
    };

    this.success = function() {
      _.modal();

      var $form = $('#hidden-login-form');

      // refresh CSRF token because api call to /auth/ changed it
      _.ajax.refreshCsrfToken();

      // fill out form with user credentials and submit it, this will tell
      // misago to redirect user back to right page, and will trigger browser's
      // key ring feature
      $form.find('input[type="hidden"]').val(_.ajax.csrfToken);
      $form.find('input[name="redirect_to"]').val(m.route());
      $form.find('input[name="username"]').val(this.username());
      $form.find('input[name="password"]').val(this.password());
      $form.submit();
    };

    this.error = function(rejection) {
      if (rejection.status === 400) {
        if (rejection.code === 'inactive_admin') {
          _.alert.info(rejection.detail);
        } else if (rejection.code === 'inactive_user') {
          _.alert.info(rejection.detail);
          self.showActivation = true;
        } else if (rejection.code === 'banned') {
          _.showBannedPage(rejection.detail);
          _.modal();
        } else {
          _.alert.error(rejection.detail);
        }
      } else {
        _.api.alert(rejection);
      }
    };
  };

  Misago.addService('form:sign-in', function(_) {
    _.form('sign-in', SignIn);
  },
  {
    after: 'forms'
  });
} (Misago.prototype));
