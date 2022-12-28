import misago from "misago/index"
import reducer from "misago/reducers/profile"
import store from "misago/services/store"

export default function initializer() {
  store.addReducer("profile", reducer, {})
}

misago.addInitializer({
  name: "reducer:profile",
  initializer: initializer,
  before: "store",
})
