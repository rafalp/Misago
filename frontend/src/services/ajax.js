export class Ajax {
  constructor() {
    this._cookieName = null;
    this._csrfToken = null;
  }

  init(cookieName) {
    this._cookieName = cookieName;
    this._csrfToken = this.getCsrfToken();
  }

  getCsrfToken() {
    if (document.cookie.indexOf(this._cookieName) !== -1) {
      var cookieRegex = new RegExp(this._cookieName + '\=([^;]*)');
      var cookie = document.cookie.match(cookieRegex)[0];
      return cookie ? cookie.split('=')[1] : null;
    } else {
      return null;
    }
  }

  request(method, url, data) {
    var self = this;
    return new Promise(function(resolve, reject) {
      var xhr = {
        url: url,
        method: method,
        headers: {
          'X-CSRFToken': self._csrfToken
        },

        data: data || {},
        dataType: 'json',

        success: function(data) {
          resolve(data);
        },

        error: function(jqXHR) {
          var rejection = jqXHR.responseJSON || {};

          rejection.status = jqXHR.status;

          if (rejection.status === 0) {
            rejection.detail = gettext("Lost connection with application.");
          }

          rejection.statusText = jqXHR.statusText;

          reject(rejection);
        }
      };

      $.ajax(xhr);
    });
  }

  get(url) {
    return this.request('GET', url);
  }

  post(url, data) {
    return this.request('POST', url, data);
  }

  patch(url, data) {
    return this.request('PATCH', url, data);
  }

  put(url, data) {
    return this.request('PUT', url, data);
  }

  delete(url) {
    return this.request('DELETE', url);
  }
}

export default new Ajax();
