import misago from "misago/index"
import dropdown from "misago/services/mobile-navbar-dropdown"

export default function initializer() {
  let element = document.getElementById("mobile-navbar-dropdown-mount")
  if (element) {
    dropdown.init(element)
  }
}

misago.addInitializer({
  name: "dropdown",
  initializer: initializer,
  before: "store",
})
