import React from "react"
import NotificationsFetch from "../NotificationsFetch"
import {
  NotificationsList,
  NotificationsListError,
  NotificationsListLoading,
} from "../NotificationsList"
import NotificationsDropdownLayout from "./NotificationsDropdownLayout"

export default class NotificationsDropdown extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      unread: false,
      url: "",
    }
  }

  getApiUrl() {
    let url = misago.get("NOTIFICATIONS_API") + "?limit=20"
    url += this.state.unread ? "&filter=unread" : ""
    return url
  }

  render = () => (
    <NotificationsDropdownLayout
      unread={this.state.unread}
      showAll={() => this.setState({ unread: false })}
      showUnread={() => this.setState({ unread: true })}
    >
      <NotificationsFetch
        filter={this.state.unread ? "unread" : "all"}
        disabled={this.props.disabled}
      >
        {({ data, loading, error }) => {
          if (loading) {
            return <NotificationsListLoading />
          }

          if (error) {
            return <NotificationsListError error={error} />
          }

          return (
            <NotificationsList
              filter={this.state.unread ? "unread" : "all"}
              items={data ? data.results : []}
            />
          )
        }}
      </NotificationsFetch>
    </NotificationsDropdownLayout>
  )
}
