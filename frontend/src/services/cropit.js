import jQuery from 'jQuery';

export class Cropit {
  init(include) {
    this._include = include;
  }

  load() {
    if (typeof jQuery.cropit === "undefined") {
      this._include.include('misago/js/jquery.cropit.js');
      return this._loadingPromise();
    } else {
      return this._loadedPromise();
    }
  }

  _loadingPromise() {
    return new Promise(function(resolve) {
      var wait = function() {
        if (typeof jQuery.cropit === "undefined") {
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
    return new Promise(function(resolve) {
      resolve();
    });
  }
}

export default new Cropit();