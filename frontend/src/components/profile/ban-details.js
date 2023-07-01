import moment from "moment"
import React from "react"
import PanelLoader from "misago/components/panel-loader"
import PanelMessage from "misago/components/panel-message"
import misago from "misago/index"
import polls from "misago/services/polls"
import title from "misago/services/page-title"

export default class extends React.Component {
  constructor(props) {
    super(props)

    if (misago.has("PROFILE_BAN")) {
      this.initWithPreloadedData(misago.pop("PROFILE_BAN"))
    } else {
      this.initWithoutPreloadedData()
    }

    this.startPolling(props.profile.api.ban)
  }

  initWithPreloadedData(ban) {
    if (ban.expires_on) {
      ban.expires_on = moment(ban.expires_on)
    }

    this.state = {
      isLoaded: true,
      ban,
    }
  }

  initWithoutPreloadedData() {
    this.state = {
      isLoaded: false,
    }
  }

  startPolling(api) {
    polls.start({
      poll: "ban-details",
      url: api,
      frequency: 90 * 1000,
      update: this.update,
      error: this.error,
    })
  }

  update = (ban) => {
    if (ban.expires_on) {
      ban.expires_on = moment(ban.expires_on)
    }

    this.setState({
      isLoaded: true,
      error: null,

      ban,
    })
  }

  error = (error) => {
    this.setState({
      isLoaded: true,
      error: error.detail,
      ban: null,
    })
  }

  componentDidMount() {
    title.set({
      title: pgettext("profile ban details title", "Ban details"),
      parent: this.props.profile.username,
    })
  }

  componentWillUnmount() {
    polls.stop("ban-details")
  }

  getUserMessage() {
    if (this.state.ban.user_message) {
      return (
        <div className="panel-body ban-message ban-user-message">
          <h4>{pgettext("profile ban details", "User-shown ban message")}</h4>
          <div
            className="lead"
            dangerouslySetInnerHTML={{
              __html: this.state.ban.user_message.html,
            }}
          />
        </div>
      )
    } else {
      return null
    }
  }

  getStaffMessage() {
    if (this.state.ban.staff_message) {
      return (
        <div className="panel-body ban-message ban-staff-message">
          <h4>{pgettext("profile ban details", "Team-shown ban message")}</h4>
          <div
            className="lead"
            dangerouslySetInnerHTML={{
              __html: this.state.ban.staff_message.html,
            }}
          />
        </div>
      )
    } else {
      return null
    }
  }

  getExpirationMessage() {
    if (this.state.ban.expires_on) {
      if (this.state.ban.expires_on.isAfter(moment())) {
        let title = interpolate(
          pgettext(
            "profile ban details",
            "This ban expires on %(expires_on)s."
          ),
          {
            expires_on: this.state.ban.expires_on.format("LL, LT"),
          },
          true
        )

        let message = interpolate(
          pgettext("profile ban details", "This ban expires %(expires_on)s."),
          {
            expires_on: this.state.ban.expires_on.fromNow(),
          },
          true
        )

        return <abbr title={title}>{message}</abbr>
      } else {
        return pgettext("profile ban details", "This ban has expired.")
      }
    } else {
      return interpolate(
        pgettext("profile ban details", "%(username)s's ban is permanent."),
        {
          username: this.props.profile.username,
        },
        true
      )
    }
  }

  getPanelBody() {
    if (this.state.ban) {
      if (Object.keys(this.state.ban).length) {
        return (
          <div>
            {this.getUserMessage()}
            {this.getStaffMessage()}

            <div className="panel-body ban-expires">
              <h4>{pgettext("profile ban details", "Ban expiration")}</h4>
              <p className="lead">{this.getExpirationMessage()}</p>
            </div>
          </div>
        )
      } else {
        return (
          <div>
            <PanelMessage
              message={pgettext(
                "profile ban details",
                "No ban is active at the moment."
              )}
            />
          </div>
        )
      }
    } else if (this.state.error) {
      return (
        <div>
          <PanelMessage icon="error_outline" message={this.state.error} />
        </div>
      )
    } else {
      return (
        <div>
          <PanelLoader />
        </div>
      )
    }
  }

  render() {
    return (
      <div className="profile-ban-details">
        <div className="panel panel-default">
          <div className="panel-heading">
            <h3 className="panel-title">
              {pgettext("profile ban details title", "Ban details")}
            </h3>
          </div>

          {this.getPanelBody()}
        </div>
      </div>
    )
  }
}
