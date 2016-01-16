import { signIn, signOut } from 'misago/reducers/auth'; // jshint ignore:line

export class Auth {
  init(store, local, modal) {
    this._store = store;
    this._local = local;
    this._modal = modal;

    // tell other tabs what auth state is because we are most current with it
    this.syncSession();

    // listen for other tabs to tell us that state changed
    this.watchState();
  }

  syncSession() {
    let state = this._store.getState().auth;
    if (state.isAuthenticated) {
      this._local.set('auth', {
        isAuthenticated: true,
        username: state.user.username
      });
    } else {
      this._local.set('auth', {
        isAuthenticated: false
      });
    }
  }

  watchState() {
    this._local.watch('auth', (newState) => {
      if (newState.isAuthenticated) {
        this._store.dispatch(signIn({
          username: newState.username
        }));
      } else {
        this._store.dispatch(signOut());
      }
    });
    this._modal.hide();
  }

  signIn(user) {
    this._store.dispatch(signIn(user));
    this._local.set('auth', {
      isAuthenticated: true,
      username: user.username
    });
    this._modal.hide();
  }

  signOut() {
    this._store.dispatch(signOut());
    this._local.set('auth', {
      isAuthenticated: false
    });
    this._modal.hide();
  }

  softSignOut() {
    this._store.dispatch(signOut(true));
    this._local.set('auth', {
      isAuthenticated: false
    });
    this._modal.hide();
  }
}

export default new Auth();