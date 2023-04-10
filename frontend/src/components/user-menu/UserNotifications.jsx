import React from "react"
import { ApiClientGet } from "../ApiClient"

export default class UserNotifications extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      open: false,
    }

    this.element = null
    this.ready = false
  }

  render() {
    const { user } = this.props

    let title = null
    if (user.unreadNotifications) {
      title = gettext("You have unread notifications!")
    } else {
      title = pgettext("navbar link", "Notifications")
    }

    return (
      <li
        className="dropdown"
        ref={(element) => {
          if (element && !this.element) {
            this.element = element

            $(element).on("show.bs.dropdown", () => {
              this.setState({ open: true })
            })

            $(element).on("hidden.bs.dropdown", () => {
              this.setState({ open: false })
            })
          }
        }}
      >
        <a
          aria-haspopup="true"
          aria-expanded="false"
          className="navbar-icon"
          data-toggle="dropdown"
          href={misago.get("NOTIFICATIONS_URL")}
          title={title}
        >
          <span className="material-icon">
            {user.unreadNotifications
              ? "notifications_active"
              : "notifications_none"}
          </span>
          {!!user.unreadNotifications && (
            <span className="badge">
              {user.unreadNotifications > 50 ? "50+" : user.unreadNotifications}
            </span>
          )}
        </a>
        <div
          className="dropdown-menu notifications-dropdown dropdown-menu-right"
          role="menu"
        >
          <ApiClientGet
            url={misago.get("NOTIFICATIONS_API") + "?filter=unread"}
            disabled={!this.state.open}
          >
            {({ data, loading, error }) => {
              if (loading) {
                return <div>Loading notifications...</div>
              }

              if (error) {
                return <div>Error!</div>
              }

              if (data) {
                return (
                  <div>
                    {data.results.map((notification) => (
                      <div key={notification.id}>
                        <a href={notification.url}>{notification.message}</a>
                      </div>
                    ))}
                  </div>
                )
              }

              return null
            }}
          </ApiClientGet>
        </div>
      </li>
    )
  }
}
