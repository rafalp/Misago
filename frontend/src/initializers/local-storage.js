import misago from "misago/index"
import storage from "misago/services/local-storage"

export default function initializer() {
  storage.init("misago_")
}

misago.addInitializer({
  name: "local-storage",
  initializer: initializer,
})
