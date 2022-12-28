import misago from "misago/index"
import reducer, { hydrate } from "misago/reducers/posts"
import store from "misago/services/store"

export default function initializer() {
  let initialState = null
  if (misago.has("POSTS")) {
    initialState = hydrate(misago.get("POSTS"))
  } else {
    initialState = {
      isLoaded: false,
      isBusy: false,
    }
  }

  store.addReducer("posts", reducer, initialState)
}

misago.addInitializer({
  name: "reducer:posts",
  initializer: initializer,
  before: "store",
})
