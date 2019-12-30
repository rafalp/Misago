import React from "react"
import { INavbarProps } from "./Navbar.types"

const Navbar: React.FC<INavbarProps> = ({ settings, user }) => {
  return (
    <nav className="navbar navbar-light bg-white">
      <div className="container-fluid">
        <a className="navbar-brand" href="#">
          {settings.forumName}
        </a>
        {user ? (
          <div>
            <img src={user.avatars[0].url} width="40" height="40" alt="" />
            {`Hello, ${user.name}`}
          </div>
        ) : (
          <div>GUEST</div>
        )}
      </div>
    </nav>
  )
}

export default Navbar
