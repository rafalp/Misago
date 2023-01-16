import React from "react"
import misago from "misago/index"
import AcceptAgreement from "misago/components/accept-agreement"
import mount from "misago/utils/mount-component"

export default function initializer(context) {
  if (document.getElementById("required-agreement-mount")) {
    mount(
      <AcceptAgreement api={context.get("REQUIRED_AGREEMENT_API")} />,
      "required-agreement-mount",
      false
    )
  }
}

misago.addInitializer({
  name: "component:accept-agreement",
  initializer: initializer,
  after: "store",
})
