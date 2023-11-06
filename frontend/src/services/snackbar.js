import { showSnackbar, hideSnackbar } from "misago/reducers/snackbar"

const HIDE_ANIMATION_LENGTH = 300
const MESSAGE_SHOW_LENGTH = 5000

export class Snackbar {
  init(store) {
    this._store = store
    this._timeout = null
  }

  alert = (message, type) => {
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

  info = (message) => {
    this.alert(message, "info")
  }

  success = (message) => {
    this.alert(message, "success")
  }

  warning = (message) => {
    this.alert(message, "warning")
  }

  error = (message) => {
    this.alert(message, "error")
  }

  // shorthand for api errors

  apiError = (rejection) => {
    let message = rejection.data ? rejection.data.detail : rejection.detail

    if (!message) {
      if (rejection.status === 0) {
        message = pgettext("api error", "Could not connect to the site.")
      } else if (rejection.status === 404) {
        message = pgettext("api error", "Action link is invalid.")
      } else {
        message = pgettext("api error", "Unknown error has occurred.")
      }
    }

    if (rejection.status === 403 && message === "Permission denied") {
      message = pgettext(
        "api error",
        "You don't have permission to perform this action."
      )
    }

    this.error(message)
  }
}

export default new Snackbar()
