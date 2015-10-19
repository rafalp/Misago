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
        fixture: ns.get(setup, 'fixture', null),
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

    // Wrap controller to store lifecycle methods
    var _controller = component.controller || noop;
    component.controller = function() {
      component.isActive = true;

      var controller = _controller.apply(component, arguments) || {};

      // wrap onunload for lifestate
      var _onunload = controller.onunload || noop;
      controller.onunload = function() {
        _onunload.apply(component, arguments);
        component.isActive = false;
      };

      return controller;
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

      var errorHandler = errorState.bind(component);

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

    this.type = 'info';
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

    if (!call.url && call.filters) {
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
    }

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
    _.user = _.models.deserialize('user', _.context.user);
  };

  Misago.addService('auth', function(_) {
    return new Auth(_);
  },
  {
    after: 'model:user'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var NoCaptcha = function() {
    var deferred = m.deferred();
    deferred.resolve();

    this.load = function() {
      return deferred.promise;
    };

    this.component = function() {
      return null;
    };

    this.value = function() {
      return null;
    };

    this.validator = function() {
      return null;
    };
  };

  var QACaptcha = function(_) {
    var self = this;

    this.loading = false;
    this.question = null;
    this.value = m.prop('asdsadsa');

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

  var ReCaptcha = function() {
    this.loading = false;
    this.question = null;

    var deferred = m.deferred();
    this.load = function() {
      return deferred.promise;
    };

    this.component = function() {
      return 'null';
    };

    this.value = function() {
      return 'pass';
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
      return captcha.component(kwargs);
    };

    this.validator = function() {
      return captcha.validator();
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
    } else {
      this._components[name] = component;
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

  Misago.addService('forum-layout', {
    factory: function(_) {
      if (_.setup.fixture) {
        m.mount(document.getElementById(_.setup.fixture),
                _.component('forum-layout'));
      }
    },

    destroy: function(_) {
      if (_.setup.fixture) {
        m.mount(document.getElementById(_.setup.fixture), null);
      }
    }
  },
  {
    before: 'start-routing'
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

  var Modal = function() {
    var self = this;

    var element = document.getElementById('misago-modal');

    // href clicks within modal should close it
    var delegateName = 'click.misago-modal';
    $(element).on(delegateName, 'a', function() {
      self.hide();
    });

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
    after: 'start-routing'
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
    this.relations = {};

    this.add = function(name, kwargs) {
      if (kwargs.class) {
        this.classes[name] = kwargs.class;
      }

      if (kwargs.deserialize) {
        this.deserializers[name] = kwargs.deserialize;
      }

      if (kwargs.relations) {
        for (var key in kwargs.relations) {
          if (kwargs.relations.hasOwnProperty(key)) {
            this.relations[name + ':' + key] = kwargs.relations[key];
          }
        }
      }
    };

    this.new = function(name, data) {
      if (this.classes[name]) {
        return new this.classes[name](data);
      } else {
        return data;
      }
    };

    this.deserialize = function(name, json) {
      if (this.relations[name]) {
        name = this.relations[name];
      }

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

  var Router = function(_) {
    var self = this;
    this.baseUrl = $('base').attr('href');

    var staticUrl = Misago.get(_.context, 'STATIC_URL', '/');
    var mediaUrl = Misago.get(_.context, 'MEDIA_URL', '/');

    // Routing
    this.urls = {};
    this.reverses = {};

    var populatePatterns = function(urlconf) {
      urlconf.patterns().forEach(function(url) {
        var finalPattern = self.baseUrl + url.pattern;
        finalPattern = finalPattern.replace('//', '/');

        self.urls[finalPattern] = _.route(url.component);
        self.reverses[url.name] = finalPattern;
      });
    };

    this.startRouting = function(urlconf, fixture) {
      populatePatterns(urlconf);
      this.fixture = fixture;

      if (_.setup.test) {
        m.route.mode = 'search';
      } else {
        m.route.mode = 'pathname';
      }
      m.route(fixture, '/', this.urls);
    };

    this.url = function(name) {
      return this.reverses[name];
    };

    // Delegate clicks
    this.delegateElement = null;

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

    var delegateName = 'click.misago-router';
    this.delegateClicks = function(element) {
      this.delegateElement = element;
      $(this.delegateElement).on(delegateName, 'a', function(e) {
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
      $(this.delegateElement).off(delegateName);
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
        component = _.route('error:banned',
          error.detail,
          _.models.deserialize('ban', error.ban));
      } else {
        component = _.route('error:403', error.detail);
      }
      m.mount(this.fixture, component);
    };

    this.error404 = function() {
      m.mount(this.fixture, _.route('error:404'));
    };

    this.error500 = function() {
      m.mount(this.fixture, _.route('error:500'));
    };

    this.error0 = function() {
      m.mount(this.fixture, _.route('error:0'));
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
    _.router.startRouting(
      Misago.urls, document.getElementById('router-fixture'));
    _.router.delegateClicks(document.getElementById(_.setup.fixture));
  },
  {
    before: '_end'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var boilerplate = function(component) {
    // Component already boilerplated (this may happen in tests)
    if (component._hasRouteBoilerplate) {
      return component;
    }
    component._hasRouteBoilerplate = true;

    // Add lifecycle hooks
    var loadingView = function () {
      var _ = this.container;
      return m('.page.page-loading',
        _.component('loader')
      );
    };

    var errorHandler = function(error) {
      if (this.isActive) {
        this.container.router.errorPage(error);
      }
    };

    return Misago.stateHooks(component, loadingView, errorHandler);
  };

  Misago.addService('routes', function(_) {
    _._routes = {};
    _.route = function(name, component) {
      if (this._routes[name]) {
        if (arguments.length > 1) {
          var argumentsArray = [this._routes[name]];
          for (var i = 1; i < arguments.length; i += 1) {
            argumentsArray.push(arguments[i]);
          }
          argumentsArray.push(this);
          return m.component.apply(undefined, argumentsArray);
        } else {
          return m.component(this._routes[name], this);
        }
      } else {
        component.container = _;
        this._routes[name] = boilerplate(component);
      }
    };
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

  var EMAIL = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
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
          return message || gettext('Enter a valid email address.');
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
              "Ensure this value has at least %(limit_value)d character (it has %(show_value)d).",
              "Ensure this value has at least %(limit_value)d characters (it has %(show_value)d).",
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
              "Ensure this value has at most %(limit_value)d character (it has %(show_value)d).",
              "Ensure this value has at most %(limit_value)d characters (it has %(show_value)d).",
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
          "Username cannot be longer than %(limit_value)s characters.",
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
    passwordMinLenght: function(settings) {
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

  var User = function(data) {
    this.id = data.id;

    this.isAuthenticated = !!this.id;
    this.isAnonymous = !this.isAuthenticated;

    this.slug = data.slug;
    this.username = data.username;

    this.acl = data.acl;
    this.rank = data.rank;
  };

  var deserializeUser = function(data) {
    if (data.joined_on) {
      data.joined_on = Misago.deserializeDatetime(data.joined_on);
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
    after: 'models'
  });
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

    return m('.page.page-error.page-error-' + error.code,
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

  var errorBanned = {
    controller: function() {
      this.container.title.set(gettext('You are banned'));
    },
    view: function(ctrl, message, ban) {
      var error_message = [];

      if (ban.message.html) {
        error_message.push(m('.lead', m.trust(ban.message.html)));
      } else if (message) {
        error_message.push(m('p.lead', message));
      } else {
        error_message.push(m('p.lead', gettext('You are banned.')));
      }

      var expirationMessage = null;
      if (ban.expires_on) {
        if (ban.expires_on.isAfter(moment())) {
          expirationMessage = interpolate(
            gettext('This ban expires %(expires_on)s.'),
            { 'expires_on': ban.expires_on.fromNow() },
            true);
        } else {
          expirationMessage = gettext('This ban has expired.');
        }
      } else {
        expirationMessage = gettext('This ban is permanent.');
      }
      error_message.push(m('p', expirationMessage));

      return m('.page.page-error.page-error-banned',
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
  };

  var error403 = {
    controller: function() {
      this.container.title.set(gettext('Page not available'));
    },
    view: function(ctrl, message) {
      if (message === "Permission denied") {
        message = gettext("You don't have permission to access this page.");
      }

      return errorPage({
        code: 403,
        icon: 'remove_circle_outline',
        message: gettext("This page is not available."),
        help: message
      });
    }
  };

  var error404 = {
    controller: function() {
      this.container.title.set(gettext('Page not found'));
    },
    view: function() {
      return errorPage({
        code: 404,
        icon: 'info_outline',
        message: gettext("Requested page could not be found."),
        help: gettext("The link you followed was incorrect or the page has been moved or deleted.")
      });
    }
  };

  var error500 = {
    controller: function() {
      this.container.title.set(gettext('Application error occured'));
    },
    view: function() {
      return errorPage({
        code: 500,
        icon: 'error_outline',
        message: gettext("Requested page could not be displayed due to an error."),
        help: gettext("Please try again later or contact site staff if error persists.")
      });
    }
  };

  var error0 = {
    controller: function() {
      this.container.title.set(gettext('Lost connection with application'));
    },
    view: function() {
      return errorPage({
        code: 0,
        icon: 'sync_problem',
        message: gettext("Could not connect to application."),
        help: gettext("This may be caused by problems with your connection or application server. Please check your internet connection and refresh page if problem persists.")
      });
    }
  };

  Misago.addService('route:error-pages', function(_) {
    _.route('error:banned', errorBanned);
    _.route('error:403', error403);
    _.route('error:404', error404);
    _.route('error:500', error500);
    _.route('error:0', error0);
  },
  {
    after: 'routes'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var index = {
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
    view: function(ctrl, _) {
      var styles = [
        'default', 'primary', 'success',
        'info', 'warning', 'danger'
      ];

      return m('.container', [
        m('h1', 'Buttons'),
        m('', styles.map(function(item) {
          return m('', [
            _.component('button', {
              class: '.btn-' + item,
              label: 'Lorem ipsum'
            }),
            _.component('button', {
              class: '.btn-' + item,
              label: 'Lorem ipsum',
              loading: true
            })
          ]);
        }))
      ]);
    }
  };

  Misago.addService('route:index', function(_) {
    _.route('index', index);
  },
  {
    after: 'routes'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var legalPageFactory = function(typeName, defaultTitle) {
    var dashedTypeName = typeName.replace(/_/g, '-');

    return {
      controller: function(_) {
        if (Misago.get(_.settings, typeName + '_link')) {
          window.location = Misago.get(_.settings, typeName + '_link');
        } else {
          this.vm.init(this, _);
        }
      },
      vm: {
        page: null,
        isReady: false,
        init: function(component, _) {
          if (this.isReady) {
            _.title.set(this.title);
          } else {
            _.title.set();
            return _.api.model('legal-page', dashedTypeName);
          }
        },
        ondata: function(page, component, _) {
          m.startComputation();

          if (page.link) {
            window.location = page.link;
          } else {
            page.title = page.title || defaultTitle;
            this.page = page;
            this.isReady = true;

            m.endComputation();

            if (component.isActive) {
              _.title.set(this.page.title);
            }
          }
        }
      },
      view: function(ctrl, _) {
        return m('.page.page-legal.page-legal-' + dashedTypeName, [
          _.component('header', {title: this.vm.page.title}),
          m('.container',
            _.component('markup', this.vm.page.body)
          )
        ]);
      }
    };
  };

  Misago.addService('route:legal-pages', function(_) {
    _.route('terms-of-service', legalPageFactory(
      'terms_of_service', gettext('Terms of service')));
    _.route('privacy-policy', legalPageFactory(
      'privacy_policy', gettext('Privacy policy')));
  },
  {
    after: 'routes'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var isMenuVisible = function(settings) {
    return [
      !!settings.forum_footnote,
      !!settings.terms_of_service,
      !!settings.terms_of_service_link,
      !!settings.privacy_policy,
      !!settings.privacy_policy_link
    ].indexOf(true) !== -1;
  };

  var footer = {
    view: function(ctrl, _) {
      var nav = null;
      if (isMenuVisible(_.settings)) {
        nav = _.component('footer:menu');
      }

      return m('footer.forum-footer', [
        m('.container',
          m('.footer-content', [
            nav,
            _.component('footer:branding')
          ])
        )
      ]);
    }
  };

  Misago.addService('component:footer', function(_) {
    _.component('footer', footer);
  },
  {
    after: 'components'
  });
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
        m('a', {href: url},
          Misago.get(_.settings, legalType + '_title', defaultTitle)
        )
      );
    } else {
      return null;
    }
  };

  var menu = {
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

      items.push(
        legalLink(_, 'terms_of_service', gettext('Terms of service')));
      items.push(
        legalLink(_, 'privacy_policy', gettext('Privacy policy')));

      return m('ul.list-inline.footer-nav', items);
    }
  };

  Misago.addService('component:footer:menu', function(_) {
    _.component('footer:menu', menu);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var branding = {
    view: function() {
      return m('a.misago-branding[href=http://misago-project.org]', [
        "powered by ", m('strong', "misago")
      ]);
    }
  };

  Misago.addService('component:footer:branding', function(_) {
    _.component('footer:branding', branding);
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

  function persistent(el, isInit, context) {
    context.retain = true;
  }

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
      var termsUrl = _.settings.terms_of_service_link;

      if (!termsUrl && _.settings.terms_of_service) {
        termsUrl = _.router.url('terms_of_service');
      }

      if (termsUrl) {
        footnote = m('a', {href: termsUrl},
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
            m('.modal-footer',
              _.component('button', {
                class: '.btn-primary.btn-block',
                submit: true,
                loading: ctrl.form.isBusy,
                label: gettext("Sign in")
              })
            )
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

  var navbar = {
    view: function(ctrl, _) {
      var style = '.navbar.navbar-default.navbar-static-top';
      return m('nav' + style + '[role="navigation"]', [
        _.component('navbar:desktop')
      ]);
    }
  };

  Misago.addService('component:navbar', function(_) {
    _.component('navbar', navbar);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var brand = {
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

  Misago.addService('component:navbar:desktop:brand', function(_) {
    _.component('navbar:desktop:brand', brand);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var menu = {
    controller: function(_) {
      return {
        showSignIn: function() {
          _.modal('sign-in');
        },

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
    view: function(ctrl, _) {
      return m('div.nav.nav-guest', [
        _.component('button', {
          class: '.navbar-btn.btn-default',
          onclick: ctrl.showSignIn,
          disabled: ctrl.isBusy,
          label: gettext('Sign in')
        }),
        _.component('button', {
          class: '.navbar-btn.btn-primary',
          onclick: ctrl.showRegister.bind(ctrl),
          loading: ctrl.isBusy,
          label: gettext('Register')
        })
      ]);
    }
  };

  Misago.addService('component:navbar:desktop:guest-menu', function(_) {
    _.component('navbar:desktop:guest-menu', menu);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var navbar = {
    view: function(ctrl, _) {
      var menu = [];

      if (_.settings.forum_branding_display) {
        menu.push(
          _.component('navbar:desktop:brand', _.settings.forum_branding_text));
      }

      menu.push(m('ul.nav.navbar-nav', [
        m('li',
          m("a", {config: m.route, href: _.router.url('index')}, 'Index')
        )
      ]));

      if (_.user.isAuthenticated) {
        menu.push(_.component('navbar:desktop:user-menu'));
      } else {
        menu.push(_.component('navbar:desktop:guest-menu'));
      }

      return m('.container.navbar-full.hidden-xs.hidden-sm', menu);
    }
  };

  Misago.addService('component:navbar:desktop', function(_) {
    _.component('navbar:desktop', navbar);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

(function (Misago) {
  'use strict';

  var menu = {
    controller: function() {
      return {
        logout: function() {
          $('#hidden-logout-form').submit();
        }
      };
    },
    view: function(ctrl, _) {
      return m('div.nav.nav-user', [
        m('p.navbar-text',
          _.user.username
        ),
        m('button.navbar-btn.btn.btn-default.navbar-right',
          {
            onclick: ctrl.logout.bind(ctrl)
          },
          gettext("Logout")
        )
      ]);
    }
  };

  Misago.addService('component:navbar:desktop:user-menu', function(_) {
    _.component('navbar:desktop:user-menu', menu);
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
      return m(
        '.alerts',
        {
          config: persistent,
          class: _.alert.isVisible ? 'in' : 'out'
        },
        m('p.alert',
          {
            class: this.classes[_.alert.type]
          },
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

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  var forumLayout = {
    view: function(ctrl, _) {
      return [
        _.component('alert'),
        _.component('navbar'),
        m('#router-fixture', {config: persistent}),
        _.component('footer'),
        _.component('modal')
      ];
    }
  };

  Misago.addService('component:layout', function(_) {
    _.component('forum-layout', forumLayout);
  },
  {
    after: 'components'
  });
}(Misago.prototype));

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

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  var modal = {
    view: function() {
      return m(
        '#misago-modal.modal.fade[role="dialog"]',
        {
          config: persistent,
          tabindex: "-1",
          "aria-labelledby": "misago-modal-label"
        }
      );
    }
  };

  Misago.addService('component:modal', function(_) {
    _.component('modal', modal);
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
        Misago.validators.passwordMinLenght(_.settings)
      ],
      'captcha': _.captcha.validator()
    };

    this.clean = function() {
      if (this.errors === null) {
        _.validate(this);
      }

      if (this.hasErrors()) {
        _.alert.error(gettext("Form contains errors"));
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
      console.log(data);
    };

    this.error = function(rejection) {
      if (rejection.status === 400) {
        if (rejection.code === 'banned') {
          _.modal();
          _.router.error403({
            message: '',
            ban: rejection.detail
          });
        } else {
          _.alert.error(gettext("Form contains errors"));
          $.extend(self.errors, rejection);
        }
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
          _.modal();
          _.router.error403({
            message: '',
            ban: rejection.detail
          });
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

(function (Misago, UrlConf) {
  'use strict';

  var urls = new UrlConf();
  urls.url('/', 'index');

  // Legal pages
  urls.url(
    '/terms-of-service/',
    'terms_of_service');

  urls.url(
    '/privacy-policy/',
    'privacy_policy');

  // Catch-all 404 not found route
  urls.url('/:rest...', 'error:404', 'not_found');

  Misago.urls = urls;
} (Misago.prototype, Misago.prototype.UrlConf));
