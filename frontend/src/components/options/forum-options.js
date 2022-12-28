import React from "react"
import Button from "misago/components/button"
import Form from "misago/components/form"
import FormGroup from "misago/components/form-group"
import Select from "misago/components/select"
import YesNoSwitch from "misago/components/yes-no-switch"
import { patch } from "misago/reducers/auth"
import ajax from "misago/services/ajax"
import title from "misago/services/page-title"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,

      is_hiding_presence: props.user.is_hiding_presence,
      limits_private_thread_invites_to:
        props.user.limits_private_thread_invites_to,
      subscribe_to_started_threads: props.user.subscribe_to_started_threads,
      subscribe_to_replied_threads: props.user.subscribe_to_replied_threads,

      errors: {},
    }

    this.privateThreadInvitesChoices = [
      {
        value: 0,
        icon: "help_outline",
        label: gettext("Everybody"),
      },
      {
        value: 1,
        icon: "done_all",
        label: gettext("Users I follow"),
      },
      {
        value: 2,
        icon: "highlight_off",
        label: gettext("Nobody"),
      },
    ]

    this.subscribeToChoices = [
      {
        value: 0,
        icon: "star_border",
        label: gettext("No"),
      },
      {
        value: 1,
        icon: "star_half",
        label: gettext("Notify"),
      },
      {
        value: 2,
        icon: "star",
        label: gettext("Notify with e-mail"),
      },
    ]
  }

  send() {
    return ajax.post(this.props.user.api.options, {
      is_hiding_presence: this.state.is_hiding_presence,
      limits_private_thread_invites_to:
        this.state.limits_private_thread_invites_to,
      subscribe_to_started_threads: this.state.subscribe_to_started_threads,
      subscribe_to_replied_threads: this.state.subscribe_to_replied_threads,
    })
  }

  handleSuccess() {
    store.dispatch(
      patch({
        is_hiding_presence: this.state.is_hiding_presence,
        limits_private_thread_invites_to:
          this.state.limits_private_thread_invites_to,
        subscribe_to_started_threads: this.state.subscribe_to_started_threads,
        subscribe_to_replied_threads: this.state.subscribe_to_replied_threads,
      })
    )
    snackbar.success(gettext("Your forum options have been changed."))
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      snackbar.error(gettext("Please reload page and try again."))
    } else {
      snackbar.apiError(rejection)
    }
  }

  componentDidMount() {
    title.set({
      title: gettext("Forum options"),
      parent: gettext("Change your options"),
    })
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <div className="panel panel-default panel-form">
          <div className="panel-heading">
            <h3 className="panel-title">{gettext("Change forum options")}</h3>
          </div>
          <div className="panel-body">
            <fieldset>
              <legend>{gettext("Privacy settings")}</legend>

              <FormGroup
                label={gettext("Hide my presence")}
                helpText={gettext(
                  "If you hide your presence, only members with permission to see hidden users will see when you are online."
                )}
                for="id_is_hiding_presence"
              >
                <YesNoSwitch
                  id="id_is_hiding_presence"
                  disabled={this.state.isLoading}
                  iconOn="visibility_off"
                  iconOff="visibility"
                  labelOn={gettext("Hide my presence from other users")}
                  labelOff={gettext("Show my presence to other users")}
                  onChange={this.bindInput("is_hiding_presence")}
                  value={this.state.is_hiding_presence}
                />
              </FormGroup>

              <FormGroup
                label={gettext("Private thread invitations")}
                for="id_limits_private_thread_invites_to"
              >
                <Select
                  id="id_limits_private_thread_invites_to"
                  disabled={this.state.isLoading}
                  onChange={this.bindInput("limits_private_thread_invites_to")}
                  value={this.state.limits_private_thread_invites_to}
                  choices={this.privateThreadInvitesChoices}
                />
              </FormGroup>
            </fieldset>

            <fieldset>
              <legend>{gettext("Automatic subscriptions")}</legend>

              <FormGroup
                label={gettext("Threads I start")}
                for="id_subscribe_to_started_threads"
              >
                <Select
                  id="id_subscribe_to_started_threads"
                  disabled={this.state.isLoading}
                  onChange={this.bindInput("subscribe_to_started_threads")}
                  value={this.state.subscribe_to_started_threads}
                  choices={this.subscribeToChoices}
                />
              </FormGroup>

              <FormGroup
                label={gettext("Threads I reply to")}
                for="id_subscribe_to_replied_threads"
              >
                <Select
                  id="id_subscribe_to_replied_threads"
                  disabled={this.state.isLoading}
                  onChange={this.bindInput("subscribe_to_replied_threads")}
                  value={this.state.subscribe_to_replied_threads}
                  choices={this.subscribeToChoices}
                />
              </FormGroup>
            </fieldset>
          </div>
          <div className="panel-footer">
            <Button className="btn-primary" loading={this.state.isLoading}>
              {gettext("Save changes")}
            </Button>
          </div>
        </div>
      </form>
    )
  }
}
