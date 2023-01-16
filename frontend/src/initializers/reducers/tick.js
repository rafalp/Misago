import misago from "misago/index"
import reducer, { initialState } from "misago/reducers/tick"
import store from "misago/services/store"

export default function initializer() {
  store.addReducer("tick", reducer, initialState)
}

misago.addInitializer({
  name: "reducer:tick",
  initializer: initializer,
  before: "store",
})
