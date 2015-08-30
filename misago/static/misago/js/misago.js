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
      this.addService('api', ns.Api);
      this.addService('outlet', ns.Outlet);
      this.addService('title', ns.PageTitle);
      this.addService('start-routing', ns.startRouting);
    };

    // Component factory
    this.component = function() {
      var arguments_array = [];
      for (var i = 0; i < arguments.length; i += 1) {
        arguments_array.push(arguments[i]);
      }

      arguments_array.push(this);
      return m.component.apply(undefined, arguments_array);
    };

    // App init/destory
    this.setup = false;
    this.init = function(setup) {
      this.setup = {
        fixture: ns.get(setup, 'fixture', null),
        in_test: ns.get(setup, 'in_test', false)
      };

      this._initServices(this._services);
    };

    this.destroy = function() {
      this._destroyServices();
    };
  };
}());


(function (ns) {
  'use strict';

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  ns.ForumLayout = {
    view: function(ctrl, _) {
      return [
        _.component(ns.ForumNavbar),
        m('#router-fixture', {config: persistent}),
        _.component(ns.ForumFooter)
      ];
    }
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  var self = {
    controller: function() {
      var _ = self.container;
      _.setTitle(_.settings.forum_index_title);
    },
    view: function() {
      return m('.container', [
        m('h1', 'Forum index page!'),
        m('p', 'Lorem ipsum dolor met sit amet elit.'),
        m('p', 'Sequar elit dolor nihi putto.')
      ]);
    }
  };
  ns.IndexPage = self;
}(Misago.prototype));

(function (ns) {
  'use strict';

  var legalPageFactory = function(type_name, default_title) {
    var dashed_type_name = type_name.replace(/_/g, '-');

    var self = {
      is_destroyed: true,
      controller: function() {
        self.is_destroyed = false;
        self.vm.init();

        return {
          onunload: function() {
            self.is_destroyed = true;
          }
        };
      },
      vm: {
        is_busy: false,
        is_ready: false,
        content: null,

        init: function() {
          var _ = self.container;

          var vm = this;
          if (vm.is_ready) {
            _.setTitle(vm.title);
          } else {
            _.setTitle();

            if (!vm.is_busy) {
              vm.is_busy = true;

              _.api.one('legal-pages', dashed_type_name).then(function(data) {
                vm.title = data.title || default_title;
                vm.body = data.body;
                vm.is_busy = false;
                vm.is_ready = true;

                if (!self.is_destroyed) {
                  _.setTitle(vm.title);
                  m.redraw();
                }
              });
            }
          }
        }
      },
      view: function() {
        var _ = this.container;

        if (this.vm.is_ready) {
          return m('.page.page-legal.page-legal-' + dashed_type_name, [
            _.component(ns.PageHeader, {title: this.vm.title}),
            m('.container',
              m.trust(this.vm.body)
            )
          ]);
        } else {
          return _.component(ns.LoadingPage);
        }
      }
    };
    return self;
  };

  ns.TermsOfServicePage = legalPageFactory(
    'terms_of_service', gettext('Terms of service'));
  ns.PrivacyPolicyPage = legalPageFactory(
    'privacy_policy', gettext('Privacy policy'));
}(Misago.prototype));

(function (ns) {
  'use strict';

  ns.Loader = {
    view: function() {
      return m('.loader.sk-folding-cube', [
        m('.sk-cube1.sk-cube'),
        m('.sk-cube2.sk-cube'),
        m('.sk-cube4.sk-cube'),
        m('.sk-cube3.sk-cube')
      ]);
    }
  };

  ns.LoadingPage = {
    view: function(ctrl, _) {
      return m('.page.page-loading',
        _.component(ns.Loader)
      );
    }
  };
} (Misago.prototype));

(function (ns) {
  'use strict';

  var setupMarkup = function(el, isInit, context) {
    context.retain = true;
  };

  ns.MisagoMarkup = {
    view: function(ctrl, content) {
      return m('article.misago-markup', {config: setupMarkup}, m.trust(content));
    }
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  ns.PageHeader = {
    view: function(ctrl, options) {
      return m('.page-header',
        m('.container', [
          m('h1', options.title),
        ])
      );
    }
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  var legalLink = function(_, legal_type, default_title) {
    var url = ns.get(_.settings, legal_type + '_link');
    if (!url && ns.get(_.settings, legal_type)) {
      url = _.router.url(legal_type);
    }

    if (url) {
      return m('li',
        m('a', {href: url}, ns.get(_.settings, legal_type + '_title', default_title))
      );
    } else {
      return null;
    }
  };

  ns.FooterNav = {
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

(function (ns) {
  'use strict';

  ns.ForumFooter = {
    view: function(ctrl, _) {
      var nav = null;
      if (ns.FooterNav.isVisible(_.settings)) {
        nav = _.component(ns.FooterNav);
      }

      return m('footer.forum-footer', [
        m('.container',
          m('.footer-content', [
            nav,
            _.component(ns.FooterMisagoBranding)
          ])
        )
      ]);
    }
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  ns.FooterMisagoBranding = {
    view: function() {
      return m('a.misago-branding[href=http://misago-project.org]', [
        "powered by ", m('strong', "misago")
      ]);
    }
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  ns.BrandFull = {
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

(function (ns) {
  'use strict';

  ns.ForumNavbar = {
    view: function(ctrl, _) {
      var desktop_navbar = [];

      if (_.settings.forum_branding_display) {
        desktop_navbar.push(_.component(ns.BrandFull, _.settings.forum_branding_text));
      }

      desktop_navbar.push(m('ul.nav.navbar-nav', [
        m('li', m("a", {config: m.route, href: _.router.url('index')}, 'Index')),
        m('li', m("a", {config: m.route, href: _.router.url('test')}, 'Test'))
      ]));

      return m('nav.navbar.navbar-default.navbar-static-top[role="navigation"]', [
        m('.container.navbar-full.hidden-xs.hidden-sm', desktop_navbar)
      ]);
    }
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  var Api = function(_) {
    // Ajax implementation
    var cookie_regex = new RegExp(_.preloaded_data.CSRF_COOKIE_NAME + '\=([^;]*)');
    this.csrf_token = ns.get(document.cookie.match(cookie_regex), 0).split('=')[1];

    this.ajax = function(method, url, data, progress) {
      var deferred = m.deferred();

      var ajax_settings = {
        url: url,
        method: method,
        headers: {
          'X-CSRFToken': this.csrf_token
        },

        data: data | {},
        dataType: 'json',

        success: function(data) {
          deferred.resolve(data);
        },
        error: function(jqXHR) {
          deferred.reject(jqXHR);
        }
      };

      if (progress) {
        return; // not implemented... yet!
      }

      $.ajax(ajax_settings);
      return deferred.promise;
    };

    this.get = function(url) {
      var preloaded_data = ns.pop(_.preloaded_data, url);
      if (preloaded_data) {
        var deferred = m.deferred();
        deferred.resolve(preloaded_data);
        return deferred.promise;
      } else {
        return this.ajax('GET', url);
      }
    };

    this.post = function(url) {
      return this.ajax('POST', url);
    };

    // API
    this.buildUrl = function(model, call, querystrings) {
      var url = _.router.base_url;
      url += 'api/' + model + '/';
      return url;
    };

    this.one = function(model, id) {
      var url = this.buildUrl(model) + id + '/';
      return this.get(url);
    };

    this.many = function(model, filters) {

    };

    this.call = function(model, call, target, data) {

    };
  };

  ns.Api = function(_) {
    return new Api(_);
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  ns.Conf = function(_) {
    _.settings = ns.get(_.preloaded_data, 'SETTINGS', {});
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  ns.Outlet = {
    factory: function(_) {
      if (_.setup.fixture) {
        m.mount(document.getElementById(_.setup.fixture),
                _.component(ns.ForumLayout));
      }
    },

    destroy: function(_) {
      if (_.setup.fixture) {
        m.mount(_.setup.fixture, null);
      }
    }
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  var Router = function(_) {
    var self = this;
    this.base_url = $('base').attr('href');

    this.static_url = ns.get(_.preloaded_data, 'STATIC_URL', '/');
    this.media_url = ns.get(_.preloaded_data, 'MEDIA_URL', '/');

    // Routing
    this.urls = {};
    this.reverses = {};

    var populatePatterns = function(urlconf) {
      urlconf.patterns().forEach(function(url) {
        // set service container on component
        url.component.container = _;

        var final_pattern = self.base_url + url.pattern;
        final_pattern = final_pattern.replace('//', '/');

        self.urls[final_pattern] = url.component;
        self.reverses[url.name] = final_pattern;
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
    this.delegate_element = null;
    this.delegate_name = 'click.misago-router';

    this.cleanUrl = function(url) {
      if (!url) { return; }

      // Is link relative?
      var is_relative = url.substr(0, 1) === '/' && url.substr(0, 2) !== '//';

      // If link contains host, validate to see if its outgoing
      if (!is_relative) {
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
      if (url.substr(0, this.base_url.length) !== this.base_url) { return; }

      // Is link to media/static/avatar server?
      if (url.substr(0, this.static_url.length) === this.static_url) { return; }

      if (url.substr(0, this.media_url.length) === this.media_url) { return; }

      var avatars_url = '/user-avatar/';
      if (url.substr(0, avatars_url.length) === avatars_url) { return; }

      return url;
    };

    this.delegateClicks = function(element) {
      this.delegate_element = element;
      $(this.delegate_element).on(this.delegate_name, 'a', function(e) {
        var clean_url = self.cleanUrl(e.target.href);
        if (clean_url) {
          if (clean_url != m.route()) {
            m.route(clean_url);
          }
          e.preventDefault();
        }
      });
    };

    this.destroy = function() {
      $(this.delegate_element).off(this.delegate_name);
    };

    // Media/Static url
    var prefixUrl = function(prefix) {
      return function(url) {
        return prefix + url;
      };
    };

    this.staticUrl = prefixUrl(ns.get(_.preloaded_data, 'STATIC_URL', '/'));
    this.mediaUrl = prefixUrl(ns.get(_.preloaded_data, 'MEDIA_URL', '/'));
  };

  ns.RouterFactory = function(_) {
    return new Router(_);
  };

  ns.startRouting = function(_) {
    _.router.startRouting(ns.urls, document.getElementById('router-fixture'));
    _.router.delegateClicks(document.getElementById(_.setup.fixture));
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  ns.PageTitle = function(_) {
    _._setTitle = function(title) {
      if (typeof title === 'string') {
        title = {title: title};
      }

      var complete_title = title.title;

      if (typeof title.page !== 'undefined' && title.page > 1) {
        complete_title += ' (' + interpolate(gettext('page %(page)s'), { page:title.page }, true) + ')';
      }

      if (typeof title.parent !== 'undefined') {
        complete_title += ' | ' + title.parent;
      }

      document.title = complete_title + ' | ' + this.settings.forum_name;
    };

    _.setTitle = function(title) {
      if (title) {
        this._setTitle(title);
      } else {
        document.title = this.settings.forum_name;
      }
    };
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

(function (ns) {
  'use strict';

  ns.startsWith = function(string, beginning) {
    return string.indexOf(beginning) === 0;
  };

  ns.endsWith = function(string, tail) {
    return string.indexOf(tail, string.length - tail.length) !== -1;
  };
}(Misago.prototype));

(function (ns) {
  'use strict';

  ns.UrlConfInvalidComponentError = function() {
    this.message = 'component argument should be array or object';
  };

  ns.UrlConf = function() {
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
        throw new ns.UrlConfInvalidComponentError();
      }

      if (pattern === '') {
        pattern = '/';
      }

      if (component instanceof ns.UrlConf) {
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

(function (ns) {
  'use strict';

  ns.loadingPage = function(_) {
    return m('.page.page-loading', _.component(ns.Loader));
  };
} (Misago.prototype));

(function (ns, UrlConf) {
  'use strict';

  var urls = new UrlConf();
  urls.url('/', ns.IndexPage, 'index');

  // Legal pages
  urls.url('/terms-of-service/', ns.TermsOfServicePage, 'terms_of_service');
  urls.url('/privacy-policy/', ns.PrivacyPolicyPage, 'privacy_policy');

  ns.urls = urls;
} (Misago.prototype, Misago.prototype.UrlConf));
