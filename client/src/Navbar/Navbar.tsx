import React from "react"
import { Button } from "../UI"
import { INavbarProps } from "./Navbar.types"

const Navbar: React.FC<INavbarProps> = ({ settings, user }) => {
  if (!settings) return null

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
          <div className="row">
            <div className="col">
              <Button text="Log-in" />
            </div>
            <div className="col">
              <Button text="Register" />
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar
