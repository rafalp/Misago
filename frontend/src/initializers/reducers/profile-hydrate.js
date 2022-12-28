import misago from "misago/index"
import { hydrate } from "misago/reducers/profile"
import store from "misago/services/store"

export default function initializer() {
  if (misago.has("PROFILE")) {
    store.dispatch(hydrate(misago.get("PROFILE")))
  }
}

misago.addInitializer({
  name: "reducer:profile-hydrate",
  initializer: initializer,
  after: "store",
})
