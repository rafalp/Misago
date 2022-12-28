import misago from "misago/index"
import reducer from "misago/reducers/participants"
import store from "misago/services/store"

export default function initializer() {
  let initialState = null
  if (misago.has("THREAD")) {
    initialState = misago.get("THREAD").participants
  }

  store.addReducer("participants", reducer, initialState || [])
}

misago.addInitializer({
  name: "reducer:participants",
  initializer: initializer,
  before: "store",
})
