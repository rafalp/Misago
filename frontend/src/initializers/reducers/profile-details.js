import misago from "misago/index"
import reducer from "misago/reducers/profile-details"
import store from "misago/services/store"

export default function initializer() {
  let initialState = null
  if (misago.has("PROFILE_DETAILS")) {
    initialState = misago.get("PROFILE_DETAILS")
  }

  store.addReducer("profile-details", reducer, initialState || {})
}

misago.addInitializer({
  name: "reducer:profile-details",
  initializer: initializer,
  before: "store",
})
