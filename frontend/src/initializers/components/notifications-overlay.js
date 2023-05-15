import React from "react"
import ReactDOM from "react-dom"
import { Provider } from "react-redux"
import NotificationsOverlay from "../../components/NotificationsOverlay"
import store from "../../services/store"

export default function initializer(context) {
  if (context.get("isAuthenticated")) {
    const root = document.getElementById("notifications-mount")
    ReactDOM.render(
      <Provider store={store.getStore()}>
        <NotificationsOverlay />
      </Provider>,
      root
    )
  }
}

misago.addInitializer({
  name: "component:notifications-overlay",
  initializer: initializer,
  after: "store",
})
