import React from "react"
import { load } from "misago/reducers/profile-details"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"

export default class extends React.Component {
  componentDidMount() {
    const { data, dispatch, user } = this.props
    if (data && data.id === user.id) return

    ajax.get(this.props.user.api.details).then(
      (data) => {
        dispatch(load(data))
      },
      (rejection) => {
        snackbar.apiError(rejection)
      }
    )
  }

  render() {
    return this.props.children
  }
}
