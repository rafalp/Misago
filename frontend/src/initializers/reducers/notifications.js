import misago from "misago/index"
import reducer, { initialState } from "../../reducers/notifications"
import store from "../../services/store"

export default function initializer(context) {
  store.addReducer("notifications", reducer, initialState)
}

misago.addInitializer({
  name: "reducer:notifications",
  initializer: initializer,
  before: "store",
})
