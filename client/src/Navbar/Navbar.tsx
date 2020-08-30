import React from "react"
import { Link } from "react-router-dom"
import { INavbarProps } from "./Navbar.types"
import NavbarCollapse from "./NavbarCollapse"
import NavbarNav from "./NavbarNav"

const Navbar: React.FC<INavbarProps> = ({ settings, user }) => {
  if (!settings) return null

  return (
    <nav className="navbar navbar-light navbar-expand-lg bg-white">
      <Link className="navbar-brand" to="/">
        {settings.forumName}
      </Link>
      <NavbarCollapse user={user}>
        <NavbarNav settings={settings} user={user} />
      </NavbarCollapse>
    </nav>
  )
}

export default Navbar
