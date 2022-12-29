import misago from "misago/index"
import ajax from "misago/services/ajax"
import captcha from "misago/services/captcha"
import include from "misago/services/include"
import snackbar from "misago/services/snackbar"

export default function initializer(context) {
  captcha.init(context, ajax, include, snackbar)
}

misago.addInitializer({
  name: "captcha",
  initializer: initializer,
})
