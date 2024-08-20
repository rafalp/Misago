import React from "react"
import ReactDOM from "react-dom"
import { Provider } from "react-redux"
import { SearchOverlay } from "../../components/search"
import store from "../../services/store"

export default function initializer(context) {
  const root = document.getElementById("search-mount")
  ReactDOM.render(
    <Provider store={store.getStore()}>
      <SearchOverlay />
    </Provider>,
    root
  )
}

misago.addInitializer({
  name: "component:search-overlay",
  initializer: initializer,
  after: "store",
})
