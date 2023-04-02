import * as React from "react"
import { connect } from "react-redux"
import misago from "misago/index"
import Categories, { select } from "../../components/categories"
import createRoot from "../../utils/createRoot"
import renderComponent from "../../utils/renderComponent"

export default function initializer() {
  const root = createRoot("categories-mount")
  if (root) {
    const CategoriesConnected = connect(select)(Categories)
    renderComponent(<CategoriesConnected />, root)
  }
}

misago.addInitializer({
  name: "component:categories",
  initializer: initializer,
  after: "store",
})
