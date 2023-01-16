import misago from "misago/index"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default function initializer() {
  snackbar.init(store)
}

misago.addInitializer({
  name: "snackbar",
  initializer: initializer,
  after: "store",
})
