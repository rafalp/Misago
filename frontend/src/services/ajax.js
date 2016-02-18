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
      let cookieRegex = new RegExp(this._cookieName + '\=([^;]*)');
      let cookie = document.cookie.match(cookieRegex)[0];
      return cookie ? cookie.split('=')[1] : null;
    } else {
      return null;
    }
  }

  request(method, url, data) {
    let self = this;
    return new Promise(function(resolve, reject) {
      let xhr = {
        url: url,
        method: method,
        headers: {
          'X-CSRFToken': self._csrfToken
        },

        data: (data ? JSON.stringify(data) : null),
        contentType: "application/json; charset=utf-8",
        dataType: 'json',

        success: function(data) {
          resolve(data);
        },

        error: function(jqXHR) {
          let rejection = jqXHR.responseJSON || {};

          rejection.status = jqXHR.status;

          if (rejection.status === 0) {
            rejection.detail = gettext("Lost connection with application.");
          }

          if (rejection.status === 404) {
            if (!rejection.detail || rejection.detail === 'NOT FOUND') {
              rejection.detail = gettext("Action link is invalid.");
            }
          }

          if (rejection.status === 500 && !rejection.detail) {
            rejection.detail = gettext("Unknown error has occured.");
          }

          rejection.statusText = jqXHR.statusText;

          reject(rejection);
        }
      };

      $.ajax(xhr);
    });
  }

  get(url, params) {
    if (params) {
      url += '?' + $.param(params);
    }
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

  upload(url, data, progress) {
    let self = this;
    return new Promise(function(resolve, reject) {
      let xhr = {
        url: url,
        method: 'POST',
        headers: {
          'X-CSRFToken': self._csrfToken
        },

        data: data,
        contentType: false,
        processData: false,

        xhr: function() {
          let xhr = new window.XMLHttpRequest();
          xhr.upload.addEventListener("progress", function(evt) {
            if (evt.lengthComputable) {
              progress(Math.round(evt.loaded / evt.total * 100));
            }
          }, false);
          return xhr;
        },

        success: function(response) {
          resolve(response);
        },

        error: function(jqXHR) {
          let rejection = jqXHR.responseJSON || {};

          rejection.status = jqXHR.status;

          if (rejection.status === 0) {
            rejection.detail = gettext("Lost connection with application.");
          }

          if (rejection.status === 404) {
            if (!rejection.detail || rejection.detail === 'NOT FOUND') {
              rejection.detail = gettext("Action link is invalid.");
            }
          }

          if (rejection.status === 500 && !rejection.detail) {
            rejection.detail = gettext("Unknown error has occured.");
          }

          rejection.statusText = jqXHR.statusText;

          reject(rejection);
        }
      };

      $.ajax(xhr);
    });
  }
}

export default new Ajax();
