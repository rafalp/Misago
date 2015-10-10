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
