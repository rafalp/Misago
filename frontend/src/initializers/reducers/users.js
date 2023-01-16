import misago from "misago/index"
import reducer from "misago/reducers/users"
import store from "misago/services/store"

export default function initializer() {
  store.addReducer("users", reducer, [])
}

misago.addInitializer({
  name: "reducer:users",
  initializer: initializer,
  before: "store",
})
