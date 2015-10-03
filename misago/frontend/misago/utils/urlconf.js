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
