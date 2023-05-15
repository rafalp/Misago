import React from "react"
import NotificationsFetch from "../NotificationsFetch"
import {
  NotificationsList,
  NotificationsListError,
  NotificationsListLoading,
} from "../NotificationsList"
import NotificationsDropdownBody from "./NotificationsDropdownBody"

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
    <NotificationsDropdownBody
      unread={this.state.unread}
      showAll={() => this.setState({ unread: false })}
      showUnread={() => this.setState({ unread: true })}
    >
      <NotificationsFetch
        filter={this.state.unread ? "unread" : "all"}
        disabled={!this.props.active}
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
    </NotificationsDropdownBody>
  )
}
