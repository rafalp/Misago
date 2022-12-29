import misago from "misago/index"
import reducer, { initialState } from "misago/reducers/snackbar"
import store from "misago/services/store"

export default function initializer() {
  store.addReducer("snackbar", reducer, initialState)
}

misago.addInitializer({
  name: "reducer:snackbar",
  initializer: initializer,
  before: "store",
})
