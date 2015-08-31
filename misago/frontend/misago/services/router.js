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

    this.staticUrl = prefixUrl(this.static_url);
    this.mediaUrl = prefixUrl(this.media_url);
  };

  ns.RouterFactory = function(_) {
    return new Router(_);
  };

  ns.startRouting = function(_) {
    _.router.startRouting(ns.urls, document.getElementById('router-fixture'));
    _.router.delegateClicks(document.getElementById(_.setup.fixture));
  };
}(Misago.prototype));
