import * as React from "react"
import misago from "misago/index"
import RequestActivationLink from "../../components/request-activation-link"
import createRoot from "../../utils/createRoot"
import renderComponent from "../../utils/renderComponent"

export default function initializer() {
  const root = createRoot("request-activation-link-mount")
  if (root) {
    renderComponent(<RequestActivationLink />, root, false)
  }
}

misago.addInitializer({
  name: "component:request-activation-link",
  initializer: initializer,
  after: "store",
})
