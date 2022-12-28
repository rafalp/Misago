import misago from "misago/index"
import reducer, { initialState } from "misago/reducers/auth"
import store from "misago/services/store"

export default function initializer(context) {
  store.addReducer(
    "auth",
    reducer,
    Object.assign(
      {
        isAuthenticated: context.get("isAuthenticated"),
        isAnonymous: !context.get("isAuthenticated"),

        user: context.get("user"),
      },
      initialState
    )
  )
}

misago.addInitializer({
  name: "reducer:auth",
  initializer: initializer,
  before: "store",
})
