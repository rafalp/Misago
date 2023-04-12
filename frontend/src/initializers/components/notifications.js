import React from "react"
import ReactDOM from "react-dom"
import Notifications from "../../components/Notifications"

export default function initializer(context) {
  const basename = misago.get("NOTIFICATIONS_URL")
  if (document.location.pathname.startsWith(basename) && context.get("isAuthenticated")) {
    const root = document.getElementById("page-mount")
    ReactDOM.render(<Notifications />, root)
  }
}

misago.addInitializer({
  name: "component:notifications",
  initializer: initializer,
  after: "store",
})
