import React from "react"
import ReactDOM from "react-dom"
import { Provider } from "react-redux"
import Navbar from "../../components/Navbar"
import store from "../../services/store"

export default function initializer(context) {
  const root = document.getElementById("misago-navbar")
  ReactDOM.render(
    <Provider store={store.getStore()}>
      <Navbar />
    </Provider>,
    root
  )
}

misago.addInitializer({
  name: "component:navbar",
  initializer: initializer,
  after: "store",
})
