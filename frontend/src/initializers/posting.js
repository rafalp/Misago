import misago from "misago/index"
import ajax from "misago/services/ajax"
import posting from "misago/services/posting"
import snackbar from "misago/services/snackbar"

export default function initializer() {
  posting.init(ajax, snackbar, document.getElementById("posting-mount"))
}

misago.addInitializer({
  name: "posting",
  initializer: initializer,
})
