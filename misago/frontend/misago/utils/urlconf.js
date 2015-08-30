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
