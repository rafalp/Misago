/* global zxcvbn */
export class Zxcvbn {
  init(include) {
    this._include = include
    this._isLoaded = false
  }

  scorePassword(password, inputs) {
    // 0-4 score, the more the stronger password
    if (this._isLoaded) {
      return zxcvbn(password, inputs).score
    }

    return 0
  }

  load() {
    if (!this._isLoaded) {
      this._include.include("misago/js/zxcvbn.js")
      return this._loadingPromise()
    } else {
      return this._loadedPromise()
    }
  }

  _loadingPromise() {
    const self = this

    return new Promise(function (resolve, reject) {
      var wait = function (tries = 0) {
        tries += 1
        if (tries > 200) {
          reject()
        } else if (typeof zxcvbn === "undefined") {
          window.setTimeout(function () {
            wait(tries)
          }, 200)
        } else {
          self._isLoaded = true
          resolve()
        }
      }
      wait()
    })
  }

  _loadedPromise() {
    // we have already loaded zxcvbn.js, resolve away!
    return new Promise(function (resolve) {
      resolve()
    })
  }
}

export default new Zxcvbn()
