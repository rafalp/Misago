import { showSnackbar, hideSnackbar } from "misago/reducers/snackbar"

const HIDE_ANIMATION_LENGTH = 300
const MESSAGE_SHOW_LENGTH = 5000

export class Snackbar {
  init(store) {
    this._store = store
    this._timeout = null
  }

  alert(message, type) {
    if (this._timeout) {
      window.clearTimeout(this._timeout)
      this._store.dispatch(hideSnackbar())

      this._timeout = window.setTimeout(() => {
        this._timeout = null
        this.alert(message, type)
      }, HIDE_ANIMATION_LENGTH)
    } else {
      this._store.dispatch(showSnackbar(message, type))
      this._timeout = window.setTimeout(() => {
        this._store.dispatch(hideSnackbar())
        this._timeout = null
      }, MESSAGE_SHOW_LENGTH)
    }
  }

  // shorthands for message types

  info(message) {
    this.alert(message, "info")
  }

  success(message) {
    this.alert(message, "success")
  }

  warning(message) {
    this.alert(message, "warning")
  }

  error(message) {
    this.alert(message, "error")
  }

  // shorthand for api errors

  apiError(rejection) {
    let message = rejection.detail

    if (!message) {
      if (rejection.status === 404) {
        message = gettext("Action link is invalid.")
      } else if (rejection.status === 401) {
        message = gettext("User is not authenticated, redirecting to Sleepio for login.")
      } else {
        message = gettext("Unknown error has occured.")
      }
    }

    if (rejection.status === 403 && message === "Permission denied") {
      message = gettext("You don't have permission to perform this action.")
    }

    this.error(message)
  }
}

export default new Snackbar()
