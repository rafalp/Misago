import React from "react"
import { Link } from "react-router"
import Li from "misago/components/li"
import FollowButton from "misago/components/profile/follow-button"
import misago from "misago/index"

export class SideNav extends React.Component {
  render() {
    return (
      <div className="list-group nav-side">
        {this.props.pages.map(page => {
          return (
            <Link
              to={this.props.baseUrl + page.component + "/"}
              className="list-group-item"
              activeClassName="active"
              key={page.component}
            >
              <span className="material-icon">{page.icon}</span>
              {page.name}
            </Link>
          )
        })}
      </div>
    )
  }
}

export function CompactNav(props) {
  return (
    <div className="page-tabs hidden-md hidden-lg">
      <div className="container">
        <ul className="nav nav-pills" role="menu">
          {props.pages.map(page => {
            return (
              <Li
                path={props.baseUrl + page.component + "/"}
                key={page.component}
              >
                <Link
                  to={props.baseUrl + page.component + "/"}
                  onClick={props.hideNav}
                >
                  <span className="material-icon">{page.icon}</span>
                  {page.name}
                </Link>
              </Li>
            )
          })}
        </ul>
      </div>
    </div>
  )
}
