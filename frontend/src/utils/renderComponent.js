import React from "react"
import { Provider } from "react-redux"
import store from "misago/services/store"

export default function renderComponent(component, root, connected = true) {
  if (connected) {
    root.render(
      <Provider store={store.getStore()}>{component}</Provider>
    )
  } else {
    root.render(component)
  }
}
