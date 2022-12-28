import misago from "misago/index"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import polls from "misago/services/polls"

export default function initializer() {
  polls.init(ajax, snackbar)
}

misago.addInitializer({
  name: "polls",
  initializer: initializer,
})
