import misago from "misago/index"
import reducer, { hydrate } from "misago/reducers/poll"
import store from "misago/services/store"

export default function initializer() {
  let initialState = null
  if (misago.has("THREAD") && misago.get("THREAD").poll) {
    initialState = hydrate(misago.get("THREAD").poll)
  } else {
    initialState = {}
  }

  store.addReducer("poll", reducer, initialState)
}

misago.addInitializer({
  name: "reducer:poll",
  initializer: initializer,
  before: "store",
})
