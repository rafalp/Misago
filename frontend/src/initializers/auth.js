import misago from "misago/index"
import auth from "misago/services/auth"
import modal from "misago/services/modal"
import store from "misago/services/store"
import storage from "misago/services/local-storage"

export default function initializer() {
  auth.init(store, storage, modal)
}

misago.addInitializer({
  name: "auth",
  initializer: initializer,
  after: "store",
})
