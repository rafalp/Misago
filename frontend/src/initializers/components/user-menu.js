import * as React from "react"
import { connect } from "react-redux"
import misago from "misago/index"
import {
  UserMenu,
  CompactUserMenu,
  select,
} from "../../components/user-menu/root"
import createRoot from "../../utils/createRoot"
import renderComponent from "../../utils/renderComponent"

export default function initializer() {
  const userMenuRoot = createRoot("user-menu-mount")
  if (userMenuRoot) {
    const UserMenuConnected = connect(select)(UserMenu)
    renderComponent(<UserMenuConnected />, userMenuRoot)
  }

  const userMenuCompactRoot = createRoot("user-menu-compact-mount")
  if (userMenuCompactRoot) {
    const CompactUserMenuConnected = connect(select)(CompactUserMenu)
    renderComponent(<CompactUserMenuConnected />, userMenuCompactRoot)
  }
}

misago.addInitializer({
  name: "component:user-menu",
  initializer: initializer,
  after: "store",
})
