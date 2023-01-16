import misago from "misago/index"
import { patch } from "misago/reducers/auth"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

const AUTH_SYNC_RATE = 45 // sync user with backend every 45 seconds

export default function initializer(context) {
  if (context.get("isAuthenticated")) {
    window.setInterval(function () {
      ajax.get(context.get("AUTH_API")).then(
        function (data) {
          store.dispatch(patch(data))
        },
        function (rejection) {
          snackbar.apiError(rejection)
        }
      )
    }, AUTH_SYNC_RATE * 1000)
  }
}

misago.addInitializer({
  name: "auth-sync",
  initializer: initializer,
  after: "auth",
})
