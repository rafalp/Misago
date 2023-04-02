import * as React from "react"
import misago from "misago/index"
import AcceptAgreement from "misago/components/accept-agreement"
import createRoot from "../../utils/createRoot"
import renderComponent from "../../utils/renderComponent"

export default function initializer(context) {
  const root = createRoot("required-agreement-mount")
  if (root) {
    renderComponent(
      <AcceptAgreement api={context.get("REQUIRED_AGREEMENT_API")} />,
      root,
      false
    )
  }
}

misago.addInitializer({
  name: "component:accept-agreement",
  initializer: initializer,
  after: "store",
})
