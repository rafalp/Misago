import { connect } from "react-redux"
import misago from "misago/index"
import AuthMessage, { select } from "misago/components/auth-message"
import mount from "misago/utils/mount-component"

export default function initializer() {
  mount(connect(select)(AuthMessage), "auth-message-mount")
}

misago.addInitializer({
  name: "component:auth-message",
  initializer: initializer,
  after: "store",
})
