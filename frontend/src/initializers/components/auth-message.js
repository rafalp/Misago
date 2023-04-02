import * as React from "react"
import { connect } from "react-redux"
import misago from "misago/index"
import AuthMessage, { select } from "../../components/auth-message"
import createRoot from "../../utils/createRoot"
import renderComponent from "../../utils/renderComponent"

export default function initializer() {
  const root = createRoot("auth-message-mount")
  if (root) {
    const AuthMessageConnected = connect(select)(AuthMessage)
    renderComponent(<AuthMessageConnected />, root)
  }
}

misago.addInitializer({
  name: "component:auth-message",
  initializer: initializer,
  after: "store",
})
