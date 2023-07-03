import React from "react"
import ChoicesControl from "./choices-control"
import Button from "misago/components/button"
import Form from "misago/components/form"
import FormGroup from "misago/components/form-group"
import YesNoSwitch from "misago/components/yes-no-switch"
import * as poll from "misago/reducers/poll"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default class extends Form {
  constructor(props) {
    super(props)

    const poll = props.poll.id
      ? props.poll
      : {
          question: "",
          choices: [
            {
              hash: "choice-10000",
              label: "",
            },
            {
              hash: "choice-20000",
              label: "",
            },
          ],
          length: 0,
          allowed_choices: 1,
          allow_revotes: 0,
          is_public: 0,
        }

    this.state = {
      isLoading: false,
      isEdit: !!poll.id,

      question: poll.question,
      choices: poll.choices,
      length: poll.length,
      allowed_choices: poll.allowed_choices,
      allow_revotes: poll.allow_revotes,
      is_public: poll.is_public,

      validators: {
        question: [],
        choices: [],
        length: [],
        allowed_choices: [],
      },

      errors: {},
    }
  }

  setChoices = (choices) => {
    this.setState((state) => {
      return {
        choices,
        errors: Object.assign({}, state.errors, { choices: null }),
      }
    })
  }

  onCancel = () => {
    let cancel = false

    // Nothing added to the poll so no changes to discard
    const formEmpty = !!(
      this.state.question === "" &&
      this.state.choices &&
      this.state.choices.every((choice) => choice.label === "") &&
      this.state.length === 0 &&
      this.state.allowed_choices === 1
    )

    if (formEmpty) {
      return this.props.close()
    }

    if (!!this.props.poll) {
      cancel = window.confirm(
        pgettext("thread poll", "Are you sure you want to discard changes?")
      )
    } else {
      cancel = window.confirm(
        pgettext("thread poll", "Are you sure you want to discard new poll?")
      )
    }

    if (cancel) {
      this.props.close()
    }
  }

  send() {
    const data = {
      question: this.state.question,
      choices: this.state.choices,
      length: this.state.length,
      allowed_choices: this.state.allowed_choices,
      allow_revotes: this.state.allow_revotes,
      is_public: this.state.is_public,
    }

    if (this.state.isEdit) {
      return ajax.put(this.props.poll.api.index, data)
    }

    return ajax.post(this.props.thread.api.poll, data)
  }

  handleSuccess(data) {
    store.dispatch(poll.replace(data))

    if (this.state.isEdit) {
      snackbar.success(pgettext("thread poll", "Poll has been edited."))
    } else {
      snackbar.success(pgettext("thread poll", "Poll has been posted."))
    }

    this.props.close()
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      if (rejection.non_field_errors) {
        rejection.allowed_choices = rejection.non_field_errors
      }

      this.setState({
        errors: Object.assign({}, rejection),
      })

      snackbar.error(gettext("Form contains errors."))
    } else {
      snackbar.apiError(rejection)
    }
  }

  render() {
    return (
      <div className="poll-form">
        <form onSubmit={this.handleSubmit}>
          <div className="panel panel-default panel-form">
            <div className="panel-heading">
              <h3 className="panel-title">
                {this.state.isEdit
                  ? pgettext("thread poll", "Edit poll")
                  : pgettext("thread poll", "Add poll")}
              </h3>
            </div>
            <div className="panel-body">
              <fieldset>
                <legend>
                  {pgettext("thread poll", "Question and choices")}
                </legend>

                <FormGroup
                  label={pgettext("thread poll", "Poll question")}
                  for="id_questions"
                  validation={this.state.errors.question}
                >
                  <input
                    className="form-control"
                    disabled={this.state.isLoading}
                    id="id_questions"
                    onChange={this.bindInput("question")}
                    type="text"
                    maxLength="255"
                    value={this.state.question}
                  />
                </FormGroup>

                <FormGroup
                  label={pgettext("thread poll", "Available choices")}
                  validation={this.state.errors.choices}
                >
                  <ChoicesControl
                    choices={this.state.choices}
                    disabled={this.state.isLoading}
                    setChoices={this.setChoices}
                  />
                </FormGroup>
              </fieldset>

              <fieldset>
                <legend>{pgettext("thread poll", "Voting")}</legend>

                <div className="row">
                  <div className="col-xs-12 col-sm-6">
                    <FormGroup
                      label={pgettext("thread poll", "Poll length")}
                      helpText={pgettext(
                        "thread poll",
                        "Enter number of days for which voting in this poll should be possible or zero to run this poll indefinitely."
                      )}
                      for="id_length"
                      validation={this.state.errors.length}
                    >
                      <input
                        className="form-control"
                        disabled={this.state.isLoading}
                        id="id_length"
                        onChange={this.bindInput("length")}
                        type="text"
                        value={this.state.length}
                      />
                    </FormGroup>
                  </div>
                  <div className="col-xs-12 col-sm-6">
                    <FormGroup
                      label={pgettext("thread poll", "Allowed choices")}
                      for="id_allowed_choices"
                      validation={this.state.errors.allowed_choices}
                    >
                      <input
                        className="form-control"
                        disabled={this.state.isLoading}
                        id="id_allowed_choices"
                        onChange={this.bindInput("allowed_choices")}
                        type="text"
                        maxLength="255"
                        value={this.state.allowed_choices}
                      />
                    </FormGroup>
                  </div>
                </div>

                <div className="row">
                  <PollPublicSwitch
                    bindInput={this.bindInput}
                    disabled={this.state.isLoading}
                    isEdit={this.state.isEdit}
                    value={this.state.is_public}
                  />
                  <div className="col-xs-12 col-sm-6">
                    <FormGroup
                      label={pgettext("thread poll", "Allow vote changes")}
                      for="id_allow_revotes"
                    >
                      <YesNoSwitch
                        id="id_allow_revotes"
                        disabled={this.state.isLoading}
                        iconOn="check"
                        iconOff="close"
                        labelOn={pgettext(
                          "thread poll",
                          "Allow participants to change their vote"
                        )}
                        labelOff={pgettext(
                          "thread poll",
                          "Don't allow participants to change their vote"
                        )}
                        onChange={this.bindInput("allow_revotes")}
                        value={this.state.allow_revotes}
                      />
                    </FormGroup>
                  </div>
                </div>
              </fieldset>
            </div>
            <div className="panel-footer text-right">
              <button
                className="btn btn-default"
                disabled={this.state.isLoading}
                onClick={this.onCancel}
                type="button"
              >
                {pgettext("thread poll", "Cancel")}
              </button>{" "}
              <Button className="btn-primary" loading={this.state.isLoading}>
                {this.state.isEdit
                  ? pgettext("thread poll", "Save changes")
                  : pgettext("thread poll", "Post poll")}
              </Button>
            </div>
          </div>
        </form>
      </div>
    )
  }
}

export function PollPublicSwitch(props) {
  if (props.isEdit) return null

  return (
    <div className="col-xs-12 col-sm-6">
      <FormGroup
        label={pgettext("thread poll", "Make voting public")}
        helpText={pgettext(
          "thread poll",
          "Making voting public will allow everyone to access detailed list of votes, showing which users voted for which choices and at which times. This option can't be changed after poll's creation. Moderators may see voting details for all polls."
        )}
        for="id_is_public"
      >
        <YesNoSwitch
          id="id_is_public"
          disabled={props.disabled}
          iconOn="visibility"
          iconOff="visibility_off"
          labelOn={pgettext("thread poll", "Votes are public")}
          labelOff={pgettext("thread poll", "Votes are hidden")}
          onChange={props.bindInput("is_public")}
          value={props.value}
        />
      </FormGroup>
    </div>
  )
}
