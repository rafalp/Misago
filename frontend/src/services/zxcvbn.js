/* global zxcvbn */
export class Zxcvbn {
  init(include) {
    this._include = include;
  }

  scorePassword(password, inputs) {
    // 0-4 score, the more the stronger password
    return zxcvbn(password, inputs).score;
  }

  load() {
    if (typeof zxcvbn === "undefined") {
      this._include.include('misago/js/zxcvbn.js');
      return this._loadingPromise();
    } else {
      return this._loadedPromise();
    }
  }

  _loadingPromise() {
    return new Promise(function(resolve) {
      var wait = function() {
        if (typeof zxcvbn === "undefined") {
          window.setTimeout(function() {
            wait();
          }, 200);
        } else {
          resolve();
        }
      };
      wait();
    });
  }

  _loadedPromise() {
    // we have already loaded zxcvbn.js, resolve away!
    return new Promise(function(resolve) {
      resolve();
    });
  }
}

export default new Zxcvbn();