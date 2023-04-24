import React from "react"
import ReactDOM from "react-dom"
import { Provider } from "react-redux"
import { SiteNavOverlay } from "../../components/SiteNav"
import store from "../../services/store"

export default function initializer(context) {
  const root = document.getElementById("site-nav-mount")
  ReactDOM.render(
    <Provider store={store.getStore()}>
      <SiteNavOverlay />
    </Provider>,
    root
  )
}

misago.addInitializer({
  name: "component:site-nav-overlay",
  initializer: initializer,
  after: "store",
})
