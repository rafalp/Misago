import misago from "misago/index"
import ajax from "misago/services/ajax"

export default function initializer() {
  ajax.init(misago.get("CSRF_COOKIE_NAME"))
}

misago.addInitializer({
  name: "ajax",
  initializer: initializer,
})
