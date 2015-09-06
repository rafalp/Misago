(function (Misago) {
  'use strict';

  var Api = function(_) {
    // Ajax implementation
    var cookie_regex = new RegExp(_.context.CSRF_COOKIE_NAME + '\=([^;]*)');
    this.csrfToken = Misago.get(document.cookie.match(cookie_regex), 0).split('=')[1];

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
          promise.resolve(data);
        },
        error: function(jqXHR) {
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
      var context = Misago.pop(_.context, url);
      if (context) {
        var deferred = m.deferred();
        deferred.resolve(context);
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
      var url = _.router.baseUrl;
      url += 'api/' + model + '/';
      return url;
    };

    this.one = function(model, id) {
      var url = this.buildUrl(model) + id + '/';
      return this.get(url);
    };

    this.many = function(model, filters) {

    };

    this.call = function(model, target, call, data) {

    };
  };

  Misago.Api = function(_) {
    return new Api(_);
  };
}(Misago.prototype));
