import React from "react"
import Button from "misago/components/button"
import { patch } from "misago/reducers/profile"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,
    }
  }

  getClassName() {
    if (this.props.profile.is_followed) {
      return this.props.className + " btn-default btn-following"
    } else {
      return this.props.className + " btn-default btn-follow"
    }
  }

  getIcon() {
    if (this.props.profile.is_followed) {
      return "favorite"
    } else {
      return "favorite_border"
    }
  }

  getLabel() {
    if (this.props.profile.is_followed) {
      return pgettext("user profile follow btn", "Following")
    } else {
      return pgettext("user profile follow btn", "Follow")
    }
  }

  action = () => {
    this.setState({
      isLoading: true,
    })

    if (this.props.profile.is_followed) {
      store.dispatch(
        patch({
          is_followed: false,
          followers: this.props.profile.followers - 1,
        })
      )
    } else {
      store.dispatch(
        patch({
          is_followed: true,
          followers: this.props.profile.followers + 1,
        })
      )
    }

    ajax.post(this.props.profile.api.follow).then(
      (data) => {
        this.setState({
          isLoading: false,
        })

        store.dispatch(patch(data))
      },
      (rejection) => {
        this.setState({
          isLoading: false,
        })
        snackbar.apiError(rejection)
      }
    )
  }

  render() {
    return (
      <Button
        className={this.getClassName()}
        disabled={this.state.isLoading}
        onClick={this.action}
      >
        <span className="material-icon">{this.getIcon()}</span>
        {this.getLabel()}
      </Button>
    )
  }
}
