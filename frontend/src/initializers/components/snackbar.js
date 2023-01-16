import { connect } from "react-redux"
import misago from "misago/index"
import { Snackbar, select } from "misago/components/snackbar"
import mount from "misago/utils/mount-component"

export default function initializer() {
  mount(connect(select)(Snackbar), "snackbar-mount")
}

misago.addInitializer({
  name: "component:snackbar",
  initializer: initializer,
  after: "snackbar",
})
