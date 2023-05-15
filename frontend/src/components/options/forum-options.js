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

const WATCH_CHOICES = [
  {
    value: 0,
    icon: "notifications_none",
    label: pgettext("watch thread choice", "No"),
  },
  {
    value: 1,
    icon: "notifications",
    label: pgettext("watch thread choice", "Yes, with on site notifications"),
  },
  {
    value: 2,
    icon: "mail",
    label: pgettext(
      "watch thread choice",
      "Yes, with on site and e-mail notifications"
    ),
  },
]

const NOTIFICATION_CHOICES = [
  {
    value: 0,
    icon: "notifications_none",
    label: pgettext("notification preference", "Don't notify"),
  },
  {
    value: 1,
    icon: "notifications",
    label: pgettext("notification preference", "Notify on site"),
  },
  {
    value: 2,
    icon: "mail",
    label: pgettext(
      "notification preference",
      "Notify on site and with e-mail"
    ),
  },
]

export default class ForumOptionsForm extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,

      is_hiding_presence: props.user.is_hiding_presence,
      limits_private_thread_invites_to:
        props.user.limits_private_thread_invites_to,

      watch_started_threads: props.user.watch_started_threads,
      watch_replied_threads: props.user.watch_replied_threads,
      watch_new_private_threads_by_followed:
        props.user.watch_new_private_threads_by_followed,
      watch_new_private_threads_by_other_users:
        props.user.watch_new_private_threads_by_other_users,
      notify_new_private_threads_by_followed:
        props.user.notify_new_private_threads_by_followed,
      notify_new_private_threads_by_other_users:
        props.user.notify_new_private_threads_by_other_users,

      errors: {},
    }

    this.privateThreadInvitesChoices = [
      {
        value: 0,
        icon: "help_outline",
        label: gettext("Anybody can invite me to their private threads"),
      },
      {
        value: 1,
        icon: "done_all",
        label: gettext(
          "Only those I follow can invite me to their private threads"
        ),
      },
      {
        value: 2,
        icon: "highlight_off",
        label: gettext("Nobody can invite me to their private threads"),
      },
    ]
  }

  send() {
    return ajax.post(this.props.user.api.options, {
      is_hiding_presence: this.state.is_hiding_presence,
      limits_private_thread_invites_to:
        this.state.limits_private_thread_invites_to,

      watch_started_threads: this.state.watch_started_threads,
      watch_replied_threads: this.state.watch_replied_threads,
      watch_new_private_threads_by_followed:
        this.state.watch_new_private_threads_by_followed,
      watch_new_private_threads_by_other_users:
        this.state.watch_new_private_threads_by_other_users,
      notify_new_private_threads_by_followed:
        this.state.notify_new_private_threads_by_followed,
      notify_new_private_threads_by_other_users:
        this.state.notify_new_private_threads_by_other_users,
    })
  }

  handleSuccess() {
    store.dispatch(
      patch({
        is_hiding_presence: this.state.is_hiding_presence,
        limits_private_thread_invites_to:
          this.state.limits_private_thread_invites_to,

        watch_started_threads: this.state.watch_started_threads,
        watch_replied_threads: this.state.watch_replied_threads,
        watch_new_private_threads_by_followed:
          this.state.watch_new_private_threads_by_followed,
        watch_new_private_threads_by_other_users:
          this.state.watch_new_private_threads_by_other_users,
        notify_new_private_threads_by_followed:
          this.state.notify_new_private_threads_by_followed,
        notify_new_private_threads_by_other_users:
          this.state.notify_new_private_threads_by_other_users,
      })
    )
    snackbar.success(gettext("Your forum options have been updated."))
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      snackbar.error(gettext("Please reload the page and try again."))
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
                label={gettext(
                  "Limit private thread invitations from other users"
                )}
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
              <legend>
                {pgettext("notifications options", "Notifications preferences")}
              </legend>

              <FormGroup
                label={pgettext(
                  "notifications options",
                  "Automatically watch threads I start"
                )}
                for="id_watch_started_threads"
              >
                <Select
                  id="id_watch_started_threads"
                  disabled={this.state.isLoading}
                  onChange={this.bindInput("watch_started_threads")}
                  value={this.state.watch_started_threads}
                  choices={WATCH_CHOICES}
                />
              </FormGroup>
              <FormGroup
                label={pgettext(
                  "notifications options",
                  "Automatically watch threads I reply to"
                )}
                for="id_watch_replied_threads"
              >
                <Select
                  id="id_watch_replied_threads"
                  disabled={this.state.isLoading}
                  onChange={this.bindInput("watch_replied_threads")}
                  value={this.state.watch_replied_threads}
                  choices={WATCH_CHOICES}
                />
              </FormGroup>
              <FormGroup
                label={pgettext(
                  "notifications options",
                  "Automatically watch new private threads I'm invited to by the members I am following"
                )}
                for="id_watch_new_private_threads_by_followed"
              >
                <Select
                  id="id_watch_new_private_threads_by_followed"
                  disabled={this.state.isLoading}
                  onChange={this.bindInput(
                    "watch_new_private_threads_by_followed"
                  )}
                  value={this.state.watch_new_private_threads_by_followed}
                  choices={WATCH_CHOICES}
                />
              </FormGroup>
              <FormGroup
                label={pgettext(
                  "notifications options",
                  "Automatically watch new private threads I'm invited to by other members"
                )}
                for="id_watch_new_private_threads_by_other_users"
              >
                <Select
                  id="id_watch_new_private_threads_by_other_users"
                  disabled={this.state.isLoading}
                  onChange={this.bindInput(
                    "watch_new_private_threads_by_other_users"
                  )}
                  value={this.state.watch_new_private_threads_by_other_users}
                  choices={WATCH_CHOICES}
                />
              </FormGroup>
              <FormGroup
                label={pgettext(
                  "notifications options",
                  "Notify me about new private thread invitations from the members I am following"
                )}
                for="id_notify_new_private_threads_by_followed"
              >
                <Select
                  id="id_notify_new_private_threads_by_followed"
                  disabled={this.state.isLoading}
                  onChange={this.bindInput(
                    "notify_new_private_threads_by_followed"
                  )}
                  value={this.state.notify_new_private_threads_by_followed}
                  choices={NOTIFICATION_CHOICES}
                />
              </FormGroup>
              <FormGroup
                label={pgettext(
                  "notifications options",
                  "Notify me about new private thread invitations from other members"
                )}
                for="id_notify_new_private_threads_by_other_users"
              >
                <Select
                  id="id_notify_new_private_threads_by_other_users"
                  disabled={this.state.isLoading}
                  onChange={this.bindInput(
                    "notify_new_private_threads_by_other_users"
                  )}
                  value={this.state.notify_new_private_threads_by_other_users}
                  choices={NOTIFICATION_CHOICES}
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
