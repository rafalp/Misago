import React from "react"
import { connect } from "react-redux"
import { close } from "../../reducers/overlay"
import NotificationsFetch from "../NotificationsFetch"
import {
  NotificationsList,
  NotificationsListError,
  NotificationsListLoading,
} from "../NotificationsList"
import NotificationsOverlayLayout from "./NotificationsOverlayLayout"

class NotificationsOverlay extends React.Component {
  constructor(props) {
    super(props)

    this.body = document.body

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

  componentDidUpdate(prevProps, prevState) {
    if (prevProps.open !== this.props.open) {
      if (this.props.open) {
        this.body.classList.add("notifications-fullscreen")
      } else {
        this.body.classList.remove("notifications-fullscreen")
      }
    }
  }

  close = () => {
    this.props.dispatch(close())
  }

  render = () => (
    <NotificationsOverlayLayout
      close={this.close}
      unread={this.state.unread}
      showAll={() => this.setState({ unread: false })}
      showUnread={() => this.setState({ unread: true })}
    >
      <NotificationsFetch
        filter={this.state.unread ? "unread" : "all"}
        disabled={!this.props.open}
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
    </NotificationsOverlayLayout>
  )
}

function select(state) {
  return { open: state.overlay.notifications }
}

const NotificationsOverlayConnected = connect(select)(NotificationsOverlay)

export default NotificationsOverlayConnected
