import React from "react"
import { Link } from "react-router"
import Li from "misago/components/li"

const ProfileNav = ({ baseUrl, page, pages }) => (
  <div className="nav-container">
    <div className="dropdown hidden-sm hidden-md hidden-lg">
      <button
        className="btn btn-default btn-block btn-outline dropdown-toggle"
        type="button"
        data-toggle="dropdown"
        aria-haspopup="true"
        aria-expanded="false"
      >
        <span className="material-icon">{page.icon}</span>
        {page.name}
      </button>
      <ul className="dropdown-menu stick-to-bottom">
        {pages.map((page) => (
          <li key={page.component}>
            <Link to={baseUrl + page.component + "/"}>
              <span className="material-icon">{page.icon}</span>
              {page.name}
            </Link>
          </li>
        ))}
      </ul>
    </div>
    <ul className="nav nav-pills hidden-xs" role="menu">
      {pages.map((page) => (
        <Li path={baseUrl + page.component + "/"} key={page.component}>
          <Link to={baseUrl + page.component + "/"}>
            <span className="material-icon">{page.icon}</span>
            {page.name}
          </Link>
        </Li>
      ))}
    </ul>
  </div>
)

export default ProfileNav
