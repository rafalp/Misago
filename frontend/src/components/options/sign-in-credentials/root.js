import React from "react"
import ChangeEmail from "misago/components/options/sign-in-credentials/change-email"
import ChangePassword from "misago/components/options/sign-in-credentials/change-password"
import misago from "misago/index"
import title from "misago/services/page-title"
import UnusablePasswordMessage from "./UnusablePasswordMessage"

export default class extends React.Component {
  componentDidMount() {
    title.set({
      title: pgettext(
        "change sign in credentials title",
        "Change email or password"
      ),
      parent: pgettext("forum options", "Change your options"),
    })
  }

  render() {
    if (!this.props.user.has_usable_password) {
      return <UnusablePasswordMessage />
    }

    return (
      <div>
        <ChangeEmail user={this.props.user} />
        <ChangePassword user={this.props.user} />

        <p className="message-line">
          <span className="material-icon">warning</span>
          <a href={misago.get("FORGOTTEN_PASSWORD_URL")}>
            {pgettext(
              "change sign in credentials link",
              "Change forgotten password"
            )}
          </a>
        </p>
      </div>
    )
  }
}
