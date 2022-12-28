import { signIn, signOut } from "misago/reducers/auth"

export class Auth {
  init(store, local, modal) {
    this._store = store
    this._local = local
    this._modal = modal

    // tell other tabs what auth state is because we are most current with it
    this.syncSession()

    // listen for other tabs to tell us that state changed
    this.watchState()
  }

  syncSession() {
    const state = this._store.getState().auth
    if (state.isAuthenticated) {
      this._local.set("auth", {
        isAuthenticated: true,
        username: state.user.username,
      })
    } else {
      this._local.set("auth", {
        isAuthenticated: false,
      })
    }
  }

  watchState() {
    const state = this._store.getState().auth
    this._local.watch("auth", (newState) => {
      if (newState.isAuthenticated) {
        this._store.dispatch(
          signIn({
            username: newState.username,
          })
        )
      } else if (state.isAuthenticated) {
        // check if we are authenticated in this tab
        // because some browser plugins prune local store
        // aggressively, forcing erroneous message to display here
        // tracking bug #955
        this._store.dispatch(signOut())
      }
    })
    this._modal.hide()
  }

  signIn(user) {
    this._store.dispatch(signIn(user))
    this._local.set("auth", {
      isAuthenticated: true,
      username: user.username,
    })
    this._modal.hide()
  }

  signOut() {
    this._store.dispatch(signOut())
    this._local.set("auth", {
      isAuthenticated: false,
    })
    this._modal.hide()
  }

  softSignOut() {
    this._store.dispatch(signOut(true))
    this._local.set("auth", {
      isAuthenticated: false,
    })
    this._modal.hide()
  }
}

export default new Auth()
