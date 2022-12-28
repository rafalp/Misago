import React from "react"
import ReactDOM from "react-dom"
import { Provider } from "react-redux"
import store from "misago/services/store"

export default function (Component, rootElementId, connected = true) {
  let rootElement = document.getElementById(rootElementId)

  let finalComponent = Component.props ? Component : <Component />

  if (rootElement) {
    if (connected) {
      ReactDOM.render(
        <Provider store={store.getStore()}>{finalComponent}</Provider>,

        rootElement
      )
    } else {
      ReactDOM.render(finalComponent, rootElement)
    }
  }
}
