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

  Misago.ajax = function(_) {
    return new Ajax(_);
  };
}(Misago.prototype));
