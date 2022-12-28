import misago from "misago/index"
import include from "misago/services/include"

export default function initializer(context) {
  include.init(context.get("STATIC_URL"))
}

misago.addInitializer({
  name: "include",
  initializer: initializer,
})
