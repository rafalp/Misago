import moment from "moment"
import misago from "misago/index"

export default function initializer() {
  moment.locale($("html").attr("lang"))
}

misago.addInitializer({
  name: "moment",
  initializer: initializer,
})
