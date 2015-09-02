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
        // set service container on component
        url.component.container = _;

        var finalPattern = self.baseUrl + url.pattern;
        finalPattern = finalPattern.replace('//', '/');

        self.urls[finalPattern] = url.component;
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
      console.log(staticUrl);
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
  };

  Misago.RouterFactory = function(_) {
    return new Router(_);
  };

  Misago.startRouting = function(_) {
    _.router.startRouting(Misago.urls, document.getElementById('router-fixture'));
    _.router.delegateClicks(document.getElementById(_.setup.fixture));
  };
}(Misago.prototype));
