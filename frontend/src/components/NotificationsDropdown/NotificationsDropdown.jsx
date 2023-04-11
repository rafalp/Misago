import React from "react"
import { ApiClientGet } from "../ApiClient"
import NotificationsDropdownBody from "./NotificationsDropdownBody"
import NotificationsDropdownEmpty from "./NotificationsDropdownEmpty"
import NotificationsDropdownError from "./NotificationsDropdownError"
import NotificationsDropdownLoading from "./NotificationsDropdownLoading"
import NotificationsDropdownList from "./NotificationsDropdownList"

export default class NotificationsDropdown extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      unread: false,
      url: "",
    }
  }

  getApiUrl() {
    let url = misago.get("NOTIFICATIONS_API") + "?limit=30"
    url += this.state.unread ? "&filter=unread" : ""
    return url
  }

  render = () => (
    <NotificationsDropdownBody
      unread={this.state.unread}
      showAll={() => this.setState({ unread: false })}
      showUnread={() => this.setState({ unread: true })}
    >
      <ApiClientGet url={this.getApiUrl()} disabled={this.props.disabled}>
        {({ data, loading, error }) => {
          if (loading) {
            return <NotificationsDropdownLoading />
          }

          if (error) {
            return <NotificationsDropdownError error={error} />
          }

          const results = data ? data.results : []

          if (results.length === 0) {
            return <NotificationsDropdownEmpty unread={this.state.unread} />
          }

          return <NotificationsDropdownList items={data ? data.results : []} />
        }}
      </ApiClientGet>
    </NotificationsDropdownBody>
  )
}
