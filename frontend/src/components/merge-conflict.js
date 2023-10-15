import React from "react"
import Button from "./button"
import Form from "./form"
import FormGroup from "./form-group"
import ajax from "misago/services/ajax"
import modal from "misago/services/modal"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,

      bestAnswer: "0",
      poll: "0",
    }
  }

  clean() {
    if (this.props.polls && this.state.poll === "0") {
      const confirmation = window.confirm(
        pgettext(
          "merge threads conflict form",
          "Are you sure you want to delete all polls?"
        )
      )
      return confirmation
    }

    return true
  }

  send() {
    const data = Object.assign({}, this.props.data, {
      best_answer: this.state.bestAnswer,
      poll: this.state.poll,
    })

    return ajax.post(this.props.api, data)
  }

  handleSuccess = (success) => {
    this.props.onSuccess(success)
    modal.hide()
  }

  handleError = (rejection) => {
    this.props.onError(rejection)
  }

  onBestAnswerChange = (event) => {
    this.changeValue("bestAnswer", event.target.value)
  }

  onPollChange = (event) => {
    this.changeValue("poll", event.target.value)
  }

  render() {
    return (
      <div className="modal-dialog" role="document">
        <div className="modal-content">
          <div className="modal-header">
            <button
              aria-label={pgettext("modal", "Close")}
              className="close"
              data-dismiss="modal"
              type="button"
            >
              <span aria-hidden="true">&times;</span>
            </button>
            <h4 className="modal-title">
              {pgettext("merge threads conflict modal title", "Merge threads")}
            </h4>
          </div>
          <form onSubmit={this.handleSubmit}>
            <div className="modal-body">
              <BestAnswerSelect
                choices={this.props.bestAnswers}
                onChange={this.onBestAnswerChange}
                value={this.state.bestAnswer}
              />
              <PollSelect
                choices={this.props.polls}
                onChange={this.onPollChange}
                value={this.state.poll}
              />
            </div>
            <div className="modal-footer">
              <button
                className="btn btn-default"
                data-dismiss="modal"
                disabled={this.state.isLoading}
                type="button"
              >
                {pgettext("merge threads conflict btn", "Cancel")}
              </button>
              <Button className="btn-primary" loading={this.state.isLoading}>
                {pgettext("merge threads conflict btn", "Merge threads")}
              </Button>
            </div>
          </form>
        </div>
      </div>
    )
  }
}

export function BestAnswerSelect({ choices, onChange, value }) {
  if (!choices) return null

  return (
    <FormGroup
      label={pgettext("merge threads conflict best answer", "Best answer")}
      helpText={pgettext(
        "merge threads conflict best answer",
        "Select the best answer for your newly merged thread. No posts will be deleted during the merge."
      )}
      for="id_best_answer"
    >
      <select
        className="form-control"
        id="id_best_answer"
        onChange={onChange}
        value={value}
      >
        {choices.map((choice) => {
          return (
            <option value={choice[0]} key={choice[0]}>
              {choice[1]}
            </option>
          )
        })}
      </select>
    </FormGroup>
  )
}

export function PollSelect({ choices, onChange, value }) {
  if (!choices) return null

  return (
    <FormGroup
      label={pgettext("merge threads conflict poll", "Poll")}
      helpText={pgettext(
        "merge threads conflict poll",
        "Select the poll for your newly merged thread. Rejected polls will be permanently deleted and cannot be recovered."
      )}
      for="id_poll"
    >
      <select
        className="form-control"
        id="id_poll"
        onChange={onChange}
        value={value}
      >
        {choices.map((choice) => {
          return (
            <option value={choice[0]} key={choice[0]}>
              {choice[1]}
            </option>
          )
        })}
      </select>
    </FormGroup>
  )
}
