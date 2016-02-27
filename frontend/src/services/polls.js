export class Polls {
  init(ajax, snackbar) {
    this._ajax = ajax;
    this._snackbar = snackbar;

    this._polls = {};
  }

  start(kwargs) {
    let poolServer = () => {
      this._polls[kwargs.poll] = kwargs;

      this._ajax.get(kwargs.url, kwargs.data || null).then((data) => {
        if (!this._polls[kwargs.poll]._stopped) {
          kwargs.update(data);

          this._polls[kwargs.poll].timeout = window.setTimeout(
            poolServer, kwargs.frequency);
        }
      }, (rejection) => {
        if (!this._polls[kwargs.poll]._stopped) {
          if (kwargs.error) {
            kwargs.error(rejection);
          } else {
            this._snackbar.apiError(rejection);
          }
        }
      });
    };

    poolServer();
  }

  stop(pollId) {
    if (this._polls[pollId]) {
      window.clearTimeout(this._polls[pollId].timeout);
      this._polls[pollId]._stopped = true;
    }
  }
}

export default new Polls();
