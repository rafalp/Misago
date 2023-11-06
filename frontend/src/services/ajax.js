export class Ajax {
  constructor() {
    this._cookieName = null
    this._csrfToken = null
    this._locks = {}
  }

  init(cookieName) {
    this._cookieName = cookieName
  }

  getCsrfToken() {
    if (document.cookie.indexOf(this._cookieName) !== -1) {
      let cookieRegex = new RegExp(this._cookieName + "=([^;]*)")
      let cookie = document.cookie.match(cookieRegex)[0]
      return cookie ? cookie.split("=")[1] : null
    } else {
      return null
    }
  }

  request(method, url, data) {
    let self = this
    return new Promise(function (resolve, reject) {
      let xhr = {
        url: url,
        method: method,
        headers: {
          "X-CSRFToken": self.getCsrfToken(),
        },

        data: data ? JSON.stringify(data) : null,
        contentType: "application/json; charset=utf-8",
        dataType: "json",

        success: function (data) {
          resolve(data)
        },

        error: function (jqXHR) {
          let rejection = jqXHR.responseJSON || {}

          rejection.status = jqXHR.status

          if (rejection.status === 0) {
            rejection.detail = pgettext(
              "ajax client error",
              "Could not connect to the site."
            )
          }

          if (rejection.status === 404) {
            if (!rejection.detail || rejection.detail === "NOT FOUND") {
              rejection.detail = pgettext(
                "ajax client error",
                "Action link is invalid."
              )
            }
          }

          if (rejection.status === 500 && !rejection.detail) {
            rejection.detail = pgettext(
              "ajax client error",
              "Unknown error has occurred."
            )
          }

          rejection.statusText = jqXHR.statusText

          reject(rejection)
        },
      }

      $.ajax(xhr)
    })
  }

  get(url, params, lock) {
    if (params) {
      url += "?" + $.param(params)
    }

    if (lock) {
      let self = this

      // update url in existing lock?
      if (this._locks[lock]) {
        this._locks[lock].url = url
      }

      // immediately dereference promise handlers without doing anything
      // we are already waiting for existing response to resolve
      if (this._locks[lock] && this._locks[lock].waiter) {
        return {
          then: function () {
            return
          },
        }

        // return promise that will begin when original one resolves
      } else if (this._locks[lock] && this._locks[lock].wait) {
        this._locks[lock].waiter = true

        return new Promise(function (resolve, reject) {
          let wait = function (url) {
            // keep waiting on promise
            if (self._locks[lock].wait) {
              window.setTimeout(function () {
                wait(url)
              }, 300)

              // poll for new url
            } else if (self._locks[lock].url !== url) {
              wait(self._locks[lock].url)

              // ajax backend for response
            } else {
              self._locks[lock].waiter = false
              self.request("GET", self._locks[lock].url).then(
                function (data) {
                  if (self._locks[lock].url === url) {
                    resolve(data)
                  } else {
                    self._locks[lock].waiter = true
                    wait(self._locks[lock].url)
                  }
                },
                function (rejection) {
                  if (self._locks[lock].url === url) {
                    reject(rejection)
                  } else {
                    self._locks[lock].waiter = true
                    wait(self._locks[lock].url)
                  }
                }
              )
            }
          }

          window.setTimeout(function () {
            wait(url)
          }, 300)
        })

        // setup new lock without waiter
      } else {
        this._locks[lock] = {
          url,
          wait: true,
          waiter: false,
        }

        return new Promise(function (resolve, reject) {
          self.request("GET", url).then(
            function (data) {
              self._locks[lock].wait = false
              if (self._locks[lock].url === url) {
                resolve(data)
              }
            },
            function (rejection) {
              self._locks[lock].wait = false
              if (self._locks[lock].url === url) {
                reject(rejection)
              }
            }
          )
        })
      }
    } else {
      return this.request("GET", url)
    }
  }

  post(url, data) {
    return this.request("POST", url, data)
  }

  patch(url, data) {
    return this.request("PATCH", url, data)
  }

  put(url, data) {
    return this.request("PUT", url, data)
  }

  delete(url, data) {
    return this.request("DELETE", url, data)
  }

  upload(url, data, progress) {
    let self = this
    return new Promise(function (resolve, reject) {
      let xhr = {
        url: url,
        method: "POST",
        headers: {
          "X-CSRFToken": self.getCsrfToken(),
        },

        data: data,
        contentType: false,
        processData: false,

        xhr: function () {
          let xhr = new window.XMLHttpRequest()
          xhr.upload.addEventListener(
            "progress",
            function (evt) {
              if (evt.lengthComputable) {
                progress(Math.round((evt.loaded / evt.total) * 100))
              }
            },
            false
          )
          return xhr
        },

        success: function (response) {
          resolve(response)
        },

        error: function (jqXHR) {
          let rejection = jqXHR.responseJSON || {}

          rejection.status = jqXHR.status

          if (rejection.status === 0) {
            rejection.detail = pgettext(
              "api error",
              "Could not connect to the site."
            )
          }

          if (rejection.status === 413 && !rejection.detail) {
            rejection.detail = pgettext(
              "api error",
              "Upload was rejected by the site as too large."
            )
          }

          if (rejection.status === 404) {
            if (!rejection.detail || rejection.detail === "NOT FOUND") {
              rejection.detail = pgettext(
                "api error",
                "Action link is invalid."
              )
            }
          }

          if (rejection.status === 500 && !rejection.detail) {
            rejection.detail = pgettext(
              "api error",
              "Unknown error has occurred."
            )
          }

          rejection.statusText = jqXHR.statusText

          reject(rejection)
        },
      }

      $.ajax(xhr)
    })
  }
}

export default new Ajax()
