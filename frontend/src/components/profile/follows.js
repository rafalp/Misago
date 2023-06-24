import React from "react"
import Followers from "misago/components/profile/followers"

export default class extends Followers {
  setSpecialProps() {
    this.PRELOADED_DATA_KEY = "PROFILE_FOLLOWS"
    this.TITLE = pgettext("profile follows title", "Follows")
    this.API_FILTER = "follows"
  }

  getLabel() {
    if (!this.state.isLoaded) {
      return pgettext("profile follows", "Loading...")
    } else if (this.state.search) {
      let message = npgettext(
        "profile follows",
        "Found %(users)s user.",
        "Found %(users)s users.",
        this.state.count
      )

      return interpolate(
        message,
        {
          users: this.state.count,
        },
        true
      )
    } else if (this.props.profile.id === this.props.user.id) {
      let message = npgettext(
        "profile follows",
        "You are following %(users)s user.",
        "You are following %(users)s users.",
        this.state.count
      )

      return interpolate(
        message,
        {
          users: this.state.count,
        },
        true
      )
    } else {
      let message = npgettext(
        "profile follows",
        "%(username)s is following %(users)s user.",
        "%(username)s is following %(users)s users.",
        this.state.count
      )

      return interpolate(
        message,
        {
          username: this.props.profile.username,
          users: this.state.count,
        },
        true
      )
    }
  }

  getEmptyMessage() {
    if (this.state.search) {
      return pgettext(
        "profile follows",
        "Search returned no users matching specified criteria."
      )
    } else if (this.props.user.id === this.props.profile.id) {
      return pgettext("profile follows", "You are not following any users.")
    } else {
      return interpolate(
        pgettext("profile follows", "%(username)s is not following any users."),
        {
          username: this.props.profile.username,
        },
        true
      )
    }
  }
}
