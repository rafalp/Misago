import React from "react"
import ReactDOM from "react-dom"
import { Provider } from "react-redux"
import Notifications from "../../components/Notifications"
import store from "../../services/store"

export default function initializer(context) {
  const basename = misago.get("NOTIFICATIONS_URL")
  if (
    document.location.pathname.startsWith(basename) &&
    !document.location.pathname.startsWith(basename + "disable-email/") &&
    context.get("isAuthenticated")
  ) {
    const root = document.getElementById("page-mount")
    ReactDOM.render(
      <Provider store={store.getStore()}>
        <Notifications />
      </Provider>,
      root
    )
  }
}

misago.addInitializer({
  name: "component:notifications",
  initializer: initializer,
  after: "store",
})
