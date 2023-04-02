import * as React from "react"
import misago from "misago"
import ResetPasswordForm from "../../components/reset-password-form"
import createRoot from "../../utils/createRoot"
import renderComponent from "../../utils/renderComponent"

export default function initializer() {
  const root = createRoot("reset-password-form-mount")
  if (root) {
    renderComponent(<ResetPasswordForm />, root, false)
  }
}

misago.addInitializer({
  name: "component:reset-password-form",
  initializer: initializer,
  after: "store",
})
