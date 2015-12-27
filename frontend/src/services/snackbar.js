import { showSnackbar, hideSnackbar } from 'misago/reducers/snackbar';

const HIDE_ANIMATION_LENGTH = 300;
const MESSAGE_SHOW_LENGTH = 5000;

export class Snackbar {
  init(store) {
    this._store = store;
    this._timeout = null;
  }

  alert(message, type) {
    if (this._timeout) {
      window.clearTimeout(this._timeout);
      this._store.dispatch(hideSnackbar());

      this._timeout = window.setTimeout(() => {
        this._timeout = null;
        this.alert(message, type);
      }, HIDE_ANIMATION_LENGTH);
    } else {
      this._store.dispatch(showSnackbar(message, type));
      this._timeout = window.setTimeout(() => {
        this._store.dispatch(hideSnackbar());
        this._timeout = null;
      }, MESSAGE_SHOW_LENGTH);
    }
  }

  // shorthands for message types
  info(message) {
    this.alert(message, 'info');
  }

  success(message) {
    this.alert(message, 'success');
  }

  warning(message) {
    this.alert(message, 'warning');
  }

  error(message) {
    this.alert(message, 'error');
  }
}

export default new Snackbar();
