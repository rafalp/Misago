import * as React from "react"
import misago from "misago/index"
import RequestPasswordReset from "../../components/request-password-reset"
import createRoot from "../../utils/createRoot"
import renderComponent from "../../utils/renderComponent"

export default function initializer() {
  const root = createRoot("request-password-reset-mount")
  if (root) {
    renderComponent(<RequestPasswordReset />, root, false)
  }
}

misago.addInitializer({
  name: "component:request-password-reset",
  initializer: initializer,
  after: "store",
})
