import React from "react"
import { Link } from "react-router"
import Li from "misago/components/li"

const UsersNav = ({ baseUrl, page, pages }) => (
  <div className="nav-container">
    <div className="dropdown hidden-sm hidden-md hidden-lg">
      <button
        className="btn btn-default btn-block btn-outline dropdown-toggle"
        type="button"
        data-toggle="dropdown"
        aria-haspopup="true"
        aria-expanded="false"
      >
        <span className="material-icon">menu</span>
        {page.name}
      </button>
      <ul className="dropdown-menu stick-to-bottom">
        {pages.map((page) => {
          const url = getPageUrl(baseUrl, page)
          return (
            <li key={url}>
              <Link to={url}>{page.name}</Link>
            </li>
          )
        })}
      </ul>
    </div>
    <ul className="nav nav-pills hidden-xs" role="menu">
      {pages.map((page) => {
        const url = getPageUrl(baseUrl, page)
        return (
          <Li path={url} key={url}>
            <Link to={url}>{page.name}</Link>
          </Li>
        )
      })}
    </ul>
  </div>
)

const getPageUrl = (baseUrl, page) => {
  let url = baseUrl
  if (page.component === "rank") {
    url += page.slug
  } else {
    url += page.component
  }
  return url + "/"
}

export default UsersNav
