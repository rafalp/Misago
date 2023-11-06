import React from "react"
import Form from "misago/components/edit-details"
import title from "misago/services/page-title"
import snackbar from "misago/services/snackbar"

export default class extends React.Component {
  componentDidMount() {
    title.set({
      title: pgettext("edit details", "Edit details"),
      parent: pgettext("forum options", "Change your options"),
    })
  }

  onSuccess = () => {
    snackbar.info(
      pgettext("profile details form", "Your details have been changed.")
    )
  }

  render() {
    return (
      <Form api={this.props.user.api.edit_details} onSuccess={this.onSuccess} />
    )
  }
}
