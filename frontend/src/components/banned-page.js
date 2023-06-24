import moment from "moment"
import React from "react"

export default class extends React.Component {
  getReasonMessage() {
    if (this.props.message.html) {
      return (
        <div
          className="lead"
          dangerouslySetInnerHTML={{
            __html: this.props.message.html,
          }}
        />
      )
    } else {
      return <p className="lead">{this.props.message.plain}</p>
    }
  }

  getExpirationMessage() {
    if (this.props.expires) {
      if (this.props.expires.isAfter(moment())) {
        let title = interpolate(
          pgettext("banned page", "This ban expires on %(expires_on)s."),
          {
            expires_on: this.props.expires.format("LL, LT"),
          },
          true
        )

        let message = interpolate(
          pgettext("banned page", "This ban expires %(expires_on)s."),
          {
            expires_on: this.props.expires.fromNow(),
          },
          true
        )

        return <abbr title={title}>{message}</abbr>
      } else {
        return pgettext("banned page", "This ban has expired.")
      }
    } else {
      return pgettext("banned page", "This ban is permanent.")
    }
  }

  render() {
    return (
      <div className="page page-error page-error-banned">
        <div className="container">
          <div className="message-panel">
            <div className="message-icon">
              <span className="material-icon">highlight_off</span>
            </div>
            <div className="message-body">
              {this.getReasonMessage()}
              <p className="message-footnote">{this.getExpirationMessage()}</p>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
