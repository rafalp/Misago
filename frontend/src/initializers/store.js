import misago from "misago/index"
import store from "misago/services/store"

export default function initializer() {
  store.init()
}

misago.addInitializer({
  name: "store",
  initializer: initializer,
  before: "_end",
})
