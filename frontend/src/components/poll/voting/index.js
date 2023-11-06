import React from "react"
import ChoicesHelp from "./help"
import ChoicesSelect from "./select"
import { getChoicesLeft, getChoiceFromHash } from "./utils"
import PollInfo from "../info"
import { Delete, Edit, getClassName } from "../results/options"
import Button from "misago/components/button"
import Form from "misago/components/form"
import * as poll from "misago/reducers/poll"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,

      choices: props.poll.choices,
      choicesLeft: getChoicesLeft(props.poll, props.poll.choices),
    }
  }

  toggleChoice = (hash) => {
    const choice = getChoiceFromHash(this.state.choices, hash)

    let choices = null
    if (!choice.selected) {
      choices = this.selectChoice(choice, hash)
    } else {
      choices = this.deselectChoice(choice, hash)
    }

    this.setState({
      choices,
      choicesLeft: getChoicesLeft(this.props.poll, choices),
    })
  }

  selectChoice = (choice, hash) => {
    const choicesLeft = getChoicesLeft(this.props.poll, this.state.choices)

    if (!choicesLeft) {
      for (const i in this.state.choices.slice()) {
        const item = this.state.choices[i]
        if (item.selected && item.hash != hash) {
          item.selected = false
          break
        }
      }
    }

    return this.state.choices.map((choice) => {
      return Object.assign({}, choice, {
        selected: choice.hash == hash ? true : choice.selected,
      })
    })
  }

  deselectChoice = (choice, hash) => {
    return this.state.choices.map((choice) => {
      return Object.assign({}, choice, {
        selected: choice.hash == hash ? false : choice.selected,
      })
    })
  }

  clean() {
    if (this.state.choicesLeft === this.props.poll.allowed_choices) {
      snackbar.error(
        pgettext("thread poll vote", "You need to select at least one choice.")
      )
      return false
    }

    return true
  }

  send() {
    let data = []
    for (const i in this.state.choices.slice()) {
      const item = this.state.choices[i]
      if (item.selected) {
        data.push(item.hash)
      }
    }

    return ajax.post(this.props.poll.api.votes, data)
  }

  handleSuccess(data) {
    store.dispatch(poll.replace(data))
    snackbar.success(pgettext("thread poll vote", "Your vote has been saved."))

    this.props.showResults()
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      snackbar.error(rejection.detail)
    } else {
      snackbar.apiError(rejection)
    }
  }

  render() {
    const controls = []

    if (this.props.poll.acl.can_vote) controls.push(0)
    if (this.props.poll.is_public || this.props.poll.acl.can_see_votes)
      controls.push(1)
    if (this.props.poll.acl.can_edit) controls.push(2)
    if (this.props.poll.acl.can_delete) controls.push(3)

    return (
      <div className="panel panel-default panel-poll">
        <form onSubmit={this.handleSubmit}>
          <div className="panel-body">
            <h2>{this.props.poll.question}</h2>
            <PollInfo poll={this.props.poll} />
            <ChoicesSelect
              choices={this.state.choices}
              toggleChoice={this.toggleChoice}
            />
            <ChoicesHelp
              choicesLeft={this.state.choicesLeft}
              poll={this.props.poll}
            />
          </div>
          <div className="panel-footer">
            <div className="row">
              <div className={getClassName(controls, 0)}>
                <Button
                  className="btn-primary btn-block btn-sm"
                  loading={this.state.isLoading}
                >
                  {pgettext("thread poll vote btn", "Save your vote")}
                </Button>
              </div>
              <div className={getClassName(controls, 1)}>
                <button
                  className="btn btn-default btn-block btn-sm"
                  disabled={this.state.isLoading}
                  onClick={this.props.showResults}
                  type="button"
                >
                  {pgettext("thread poll vote btn", "See results")}
                </button>
              </div>
              <Edit
                controls={controls}
                poll={this.props.poll}
                thread={this.props.thread}
                onClick={this.props.edit}
              />
              <Delete controls={controls} poll={this.props.poll} />
            </div>
          </div>
        </form>
      </div>
    )
  }
}
