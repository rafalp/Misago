import React from "react"
import Form from "./form"
import GroupsList from "./groups-list"
import Header from "./header"
import ProfileDetailsData from "misago/data/profile-details"
import { load as loadDetails } from "misago/reducers/profile-details"
import title from "misago/services/page-title"
import snackbar from "misago/services/snackbar"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      editing: false,
    }
  }

  componentDidMount() {
    title.set({
      title: pgettext("profile details title", "Details"),
      parent: this.props.profile.username,
    })
  }

  onCancel = () => {
    this.setState({ editing: false })
  }

  onEdit = () => {
    this.setState({ editing: true })
  }

  onSuccess = (newDetails) => {
    const { dispatch, isAuthenticated, profile } = this.props

    let message = null
    if (isAuthenticated) {
      message = pgettext(
        "profile details form",
        "Your details have been changed."
      )
    } else {
      message = interpolate(
        pgettext(
          "profile details form",
          "%(username)s's details have been changed."
        ),
        {
          username: profile.username,
        },
        true
      )
    }

    snackbar.info(message)
    dispatch(loadDetails(newDetails))
    this.setState({ editing: false })
  }

  render() {
    const { dispatch, isAuthenticated, profile, profileDetails } = this.props
    const loading = profileDetails.id !== profile.id

    return (
      <ProfileDetailsData
        data={profileDetails}
        dispatch={dispatch}
        user={profile}
      >
        <div className="profile-details">
          <Header
            onEdit={this.onEdit}
            showEditButton={!!profileDetails.edit && !this.state.editing}
          />
          <GroupsList
            display={!this.state.editing}
            groups={profileDetails.groups}
            isAuthenticated={isAuthenticated}
            loading={loading}
            profile={profile}
          />
          <Form
            api={profile.api.edit_details}
            dispatch={dispatch}
            display={this.state.editing}
            onCancel={this.onCancel}
            onSuccess={this.onSuccess}
          />
        </div>
      </ProfileDetailsData>
    )
  }
}
