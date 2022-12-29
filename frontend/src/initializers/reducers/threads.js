import misago from "misago/index"
import reducer from "misago/reducers/threads"
import store from "misago/services/store"

export default function initializer() {
  store.addReducer("threads", reducer, [])
}

misago.addInitializer({
  name: "reducer:threads",
  initializer: initializer,
  before: "store",
})
