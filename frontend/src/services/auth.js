import { signIn, signOut } from 'misago/reducers/auth'; // jshint ignore:line

export class Auth {
  init(store, local) {
    this._store = store;
    this._local = local;

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
  }

  signIn(user) {
    this._store.dispatch(signIn(user));
    this._local.set('auth', {
      isAuthenticated: true,
      username: user.username
    });
  }

  signOut() {
    this._store.dispatch(signOut());
    this._local.set('auth', {
      isAuthenticated: false
    });
  }
}

export default new Auth();