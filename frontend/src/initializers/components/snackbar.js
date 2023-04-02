import * as React from "react"
import { connect } from "react-redux"
import misago from "misago/index"
import { Snackbar, select } from "../../components/snackbar"
import createRoot from "../../utils/createRoot"
import renderComponent from "../../utils/renderComponent"

export default function initializer() {
  const root = createRoot("snackbar-mount")
  if (root) {
    const SnackbarConnected = connect(select)(Snackbar)
    renderComponent(<SnackbarConnected />, root)
  }
}

misago.addInitializer({
  name: "component:snackbar",
  initializer: initializer,
  after: "snackbar",
})
