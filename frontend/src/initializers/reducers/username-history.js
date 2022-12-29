import misago from "misago/index"
import reducer from "misago/reducers/username-history"
import store from "misago/services/store"

export default function initializer() {
  store.addReducer("username-history", reducer, [])
}

misago.addInitializer({
  name: "reducer:username-history",
  initializer: initializer,
  before: "store",
})
