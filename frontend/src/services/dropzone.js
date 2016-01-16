import jQuery from 'jQuery';

export class Dropzone {
  init(include) {
    this._include = include;
  }

  load() {
    if (typeof jQuery.dropzone === "undefined") {
      this._include.include('misago/js/dropzone.js');
      return this._loadingPromise();
    } else {
      return this._loadedPromise();
    }
  }

  _loadingPromise() {
    return new Promise(function(resolve) {
      var wait = function() {
        if (typeof jQuery.dropzone === "undefined") {
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

export default new Dropzone();