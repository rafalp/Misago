import misago from "misago/index"
import reducer from "misago/reducers/selection"
import store from "misago/services/store"

export default function initializer() {
  store.addReducer("selection", reducer, [])
}

misago.addInitializer({
  name: "reducer:selection",
  initializer: initializer,
  before: "store",
})
