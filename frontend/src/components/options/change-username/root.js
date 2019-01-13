import moment from "moment"
import React from "react"
import FormLoading from "misago/components/options/change-username/form-loading"
import FormLocked from "misago/components/options/change-username/form-locked"
import Form from "misago/components/options/change-username/form"
import UsernameHistory from "misago/components/username-history/root"
import misago from "misago/index"
import { hydrate, addNameChange } from "misago/reducers/username-history"
import { updateUsername } from "misago/reducers/users"
import ajax from "misago/services/ajax"
import title from "misago/services/page-title"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      isLoaded: false,
      options: null
    }
  }

  componentDidMount() {
    title.set({
      title: gettext("Change username"),
      parent: gettext("Change your options")
    })

    Promise.all([
      ajax.get(this.props.user.api.username),
      ajax.get(misago.get("USERNAME_CHANGES_API"), { user: this.props.user.id })
    ]).then(data => {
      store.dispatch(hydrate(data[1].results))

      this.setState({
        isLoaded: true,
        options: {
          changes_left: data[0].changes_left,
          length_min: data[0].length_min,
          length_max: data[0].length_max,
          next_on: data[0].next_on ? moment(data[0].next_on) : null
        }
      })
    })
  }

  onComplete = (username, slug, options) => {
    this.setState({
      options
    })

    store.dispatch(
      addNameChange({ username, slug }, this.props.user, this.props.user)
    )
    store.dispatch(updateUsername(this.props.user, username, slug))

    snackbar.success(gettext("Your username has been changed successfully."))
  }

  getChangeForm() {
    if (!this.state.isLoaded) {
      return <FormLoading />
    }

    if (this.state.options.changes_left === 0) {
      return <FormLocked options={this.state.options} />
    }

    return (
      <Form
        complete={this.onComplete}
        options={this.state.options}
        user={this.props.user}
      />
    )
  }

  render() {
    return (
      <div>
        {this.getChangeForm()}
        <UsernameHistory
          changes={this.props["username-history"]}
          isLoaded={this.state.isLoaded}
        />
      </div>
    )
  }
}
