import React from "react"
import ReactDOM from "react-dom"
import { Provider } from "react-redux"
import { UserNavOverlay } from "../../components/UserNav"
import store from "../../services/store"

export default function initializer(context) {
  const root = document.getElementById("user-nav-mount")
  ReactDOM.render(
    <Provider store={store.getStore()}>
      <UserNavOverlay />
    </Provider>,
    root
  )
}

misago.addInitializer({
  name: "component:user-nav-overlay",
  initializer: initializer,
  after: "store",
})
