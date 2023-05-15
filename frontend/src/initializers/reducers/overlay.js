import misago from "misago/index"
import reducer, { initialState } from "../../reducers/overlay"
import store from "../../services/store"

export default function initializer(context) {
  store.addReducer("overlay", reducer, initialState)
}

misago.addInitializer({
  name: "reducer:overlay",
  initializer: initializer,
  before: "store",
})
