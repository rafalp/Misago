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
      if (runningGets[url]) {
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

    this.buildApiUrl = function(path) {
      var url = _.setup.api;

      if (path) {
        url += path.join('/') + '/';
      }

      return url;
    };

    // Shorthand for handling backend errors
    this.error = function(rejection) {
      if (rejection.ban) {
        _.showBannedPage(rejection.ban);
        _.modal();
      } else {
        this.alert(rejection);
      }
    };

    this.alert = function(rejection) {
      var message = gettext("Unknown error has occured.");

      if (rejection.status === 0) {
        message = gettext("Lost connection with application.");
      }

      if (rejection.status === 400 && rejection.detail) {
        message = rejection.detail;
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

  Misago.addService('ajax', function(_) {
    return new Ajax(_);
  });
}(Misago.prototype));
