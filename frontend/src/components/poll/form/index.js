// jshint ignore:start
import React from 'react';
import ChoicesControl from './choices-control';
import Button from 'misago/components/button';
import Form from 'misago/components/form';
import FormGroup from 'misago/components/form-group';
import YesNoSwitch from 'misago/components/yes-no-switch';
import * as poll from 'misago/reducers/poll';
import ajax from 'misago/services/ajax';
import posting from 'misago/services/posting';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';

export default class extends Form {
  constructor(props) {
    super(props);

    const poll = props.poll || {
      question: '',
      choices: [
        {
          hash: 'choice-10000',
          label: ''
        },
        {
          hash: 'choice-20000',
          label: ''
        }
      ],
      length: 0,
      allowed_choices: 1,
      allow_revotes: 0,
      is_public: 0
    };

    this.state = {
      isLoading: false,
      isEdit: !!poll.question,

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
        allowed_choices: []
      },

      errors: {}
    };
  }

  setChoices = (choices) => {
    const errors = Object.assign({}, errors, {choices: null});

    this.setState({
      choices,
      errors
    });
  };

  onCancel = () => {
    const cancel = confirm(gettext("Are you sure you want to discard poll?"));
    if (cancel) {
      posting.close();
    }
  };

  send() {
    const data = {
      question: this.state.question,
      choices: this.state.choices,
      length: this.state.length,
      allowed_choices: this.state.allowed_choices,
      allow_revotes: this.state.allow_revotes,
      is_public: this.state.is_public
    };

    if (this.state.isEdit) {
      return ajax.put(this.props.poll.api.index, data);
    } else {
      return ajax.post(this.props.thread.api.poll, data);
    }
  }

  handleSuccess(data) {
    store.dispatch(poll.replace(data));

    if (this.state.isEdit) {
      snackbar.success(gettext("Poll has been edited."));
    } else {
      snackbar.success(gettext("Poll has been posted."));
    }

    posting.close();
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      if (rejection.non_field_errors) {
        rejection.allowed_choices = rejection.non_field_errors;
      }

      this.setState({
        'errors': Object.assign({}, rejection)
      });

      snackbar.error(gettext("Form contains errors."));
    } else {
      snackbar.apiError(rejection);
    }
  }

  render() {
    return (
      <div className="poll-form">
        <div className="container">
          <form onSubmit={this.handleSubmit} className="form-horizontal">
            <div className="panel panel-default panel-form">
              <div className="panel-body">

                <fieldset>
                  <legend>{gettext("Question and choices")}</legend>

                  <FormGroup
                    label={gettext("Poll question")}
                    for="id_questions"
                    labelClass="col-sm-4" controlClass="col-sm-8"
                    validation={this.state.errors.question}
                  >
                    <input
                      className="form-control"
                      disabled={this.state.isLoading}
                      id="id_questions"
                      onChange={this.bindInput('question')}
                      type="text"
                      maxLength="255"
                      value={this.state.question}
                    />
                  </FormGroup>

                  <FormGroup
                    label={gettext("Available choices")}
                    labelClass="col-sm-4" controlClass="col-sm-8"
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
                  <legend>{gettext("Voting")}</legend>

                  <FormGroup
                    label={gettext("Poll length")}
                    helpText={gettext("Enter number of days for which voting in this poll should be possible or zero to run this poll indefinitely.")}
                    for="id_length"
                    labelClass="col-sm-4" controlClass="col-sm-8"
                    validation={this.state.errors.length}
                  >
                    <input
                      className="form-control"
                      disabled={this.state.isLoading}
                      id="id_length"
                      onChange={this.bindInput('length')}
                      type="text"
                      value={this.state.length}
                    />
                  </FormGroup>

                  <FormGroup
                    label={gettext("Allowed choices")}
                    for="id_allowed_choices"
                    labelClass="col-sm-4" controlClass="col-sm-8"
                    validation={this.state.errors.allowed_choices}
                  >
                    <input
                      className="form-control"
                      disabled={this.state.isLoading}
                      id="id_allowed_choices"
                      onChange={this.bindInput('allowed_choices')}
                      type="text"
                      maxLength="255"
                      value={this.state.allowed_choices}
                    />
                  </FormGroup>

                  <FormGroup
                    label={gettext("Allow vote changes")}
                    for="id_allow_revotes"
                    labelClass="col-sm-4" controlClass="col-sm-8"
                  >
                    <YesNoSwitch
                      id="id_allow_revotes"
                      disabled={this.state.isLoading}
                      iconOn="check"
                      iconOff="close"
                      labelOn={gettext("Allow participants to change their vote")}
                      labelOff={gettext("Don't allow participants to change their vote")}
                      onChange={this.bindInput('allow_revotes')}
                      value={this.state.allow_revotes}
                    />
                  </FormGroup>

                  <PollPublicSwitch
                    bindInput={this.bindInput}
                    disabled={this.state.isLoading}
                    isEdit={this.state.isEdit}
                    value={this.state.is_public}
                  />

                </fieldset>

              </div>
              <div className="panel-footer">
                <div className="row">
                  <div className="col-sm-8 col-sm-offset-4">

                    <Button
                      className="btn-primary"
                      loading={this.state.isLoading}
                    >
                      {this.state.isEdit ? gettext("Save changes") : gettext("Post poll")}
                    </Button>
                    &nbsp;
                    <button
                      className="btn btn-default"
                      disabled={this.state.isLoading}
                      onClick={this.onCancel}
                      type="button"
                    >
                      {gettext("Cancel")}
                    </button>

                  </div>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    );
  }
}

export function PollPublicSwitch(props) {
  if (props.isEdit) return null;

  return (
    <FormGroup
      label={gettext("Make voting public")}
      helpText={gettext("Making voting public will allow everyone to access detailed list of votes, showing which users voted for which choices and at which times. This option can't be changed after poll's creation. Moderators may see voting details for all polls.")}
      for="id_is_public"
      labelClass="col-sm-4" controlClass="col-sm-8"
    >
      <YesNoSwitch
        id="id_is_public"
        disabled={props.disabled}
        iconOn="visibility"
        iconOff="visibility_off"
        labelOn={gettext("Votes are public")}
        labelOff={gettext("Votes are hidden")}
        onChange={props.bindInput('is_public')}
        value={props.value}
      />
    </FormGroup>
  );
}