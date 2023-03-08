import React from "react"
import Modal from "./modal"
import * as poll from "misago/reducers/poll"
import * as thread from "misago/reducers/thread"
import ajax from "misago/services/ajax"
import modal from "misago/services/modal"
import posting from "misago/services/posting"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default function (props) {
  const { isPollOver, poll, showVoting, thread } = props

  if (!isVisible(isPollOver, poll.acl, poll)) return null

  const controls = []

  const canVote = poll.acl.can_vote
  const canChangeVote = !poll.hasSelectedChoices || poll.allow_revotes

  if (canVote && canChangeVote) controls.push(0)
  if (poll.is_public || poll.acl.can_see_votes) controls.push(1)
  if (poll.acl.can_edit) controls.push(2)
  if (poll.acl.can_delete) controls.push(3)

  return (
    <div className="row poll-options">
      <ChangeVote
        controls={controls}
        isPollOver={isPollOver}
        poll={poll}
        showVoting={showVoting}
      />
      <SeeVotes controls={controls} poll={poll} />
      <Edit
        controls={controls}
        poll={poll}
        thread={thread}
        onClick={props.edit}
      />
      <Delete controls={controls} poll={poll} />
    </div>
  )
}

export function isVisible(isPollOver, acl, poll) {
  return (
    poll.is_public ||
    acl.can_delete ||
    acl.can_edit ||
    acl.can_see_votes ||
    (acl.can_vote &&
      !isPollOver &&
      (!poll.hasSelectedChoices || poll.allow_revotes))
  )
}

export function getClassName(controls, control) {
  let className = "col-xs-6"

  if (controls.length === 1) {
    className = "col-xs-12"
  }

  if (controls.length === 3 && controls[0] === control) {
    className = "col-xs-12"
  }

  return className + " col-sm-3 col-md-2"
}

export function ChangeVote(props) {
  const canVote = props.poll.acl.can_vote
  const canChangeVote =
    !props.poll.hasSelectedChoices || props.poll.allow_revotes

  if (!(canVote && canChangeVote)) return null

  return (
    <div className={getClassName(props.controls, 0)}>
      <button
        className="btn btn-default btn-block btn-sm"
        disabled={props.poll.isBusy}
        onClick={props.showVoting}
        type="button"
      >
        {pgettext("thread poll", "Vote")}
      </button>
    </div>
  )
}

export class SeeVotes extends React.Component {
  onClick = () => {
    modal.show(<Modal poll={this.props.poll} />)
  }

  render() {
    const seeVotes =
      this.props.poll.is_public || this.props.poll.acl.can_see_votes
    if (!seeVotes) return null

    return (
      <div className={getClassName(this.props.controls, 1)}>
        <button
          className="btn btn-default btn-block btn-sm"
          disabled={this.props.poll.isBusy}
          onClick={this.onClick}
          type="button"
        >
          {pgettext("thread poll", "See votes")}
        </button>
      </div>
    )
  }
}

export function Edit(props) {
  if (!props.poll.acl.can_edit) return null

  return (
    <div className={getClassName(props.controls, 2)}>
      <button
        className="btn btn-default btn-block btn-sm"
        disabled={props.poll.isBusy}
        onClick={props.onClick}
        type="button"
      >
        {pgettext("thread poll", "Edit")}
      </button>
    </div>
  )
}

export class Delete extends React.Component {
  onClick = () => {
    const deletePoll = window.confirm(
      pgettext(
        "thread poll",
        "Are you sure you want to delete this poll? This action is not reversible."
      )
    )
    if (!deletePoll) return false

    store.dispatch(poll.busy())

    ajax
      .delete(this.props.poll.api.index)
      .then(this.handleSuccess, this.handleError)
  }

  handleSuccess = (newThreadAcl) => {
    snackbar.success(pgettext("thread poll", "Poll has been deleted"))
    store.dispatch(poll.remove())
    store.dispatch(thread.updateAcl(newThreadAcl))
  }

  handleError = (rejection) => {
    snackbar.apiError(rejection)
    store.dispatch(poll.release())
  }

  render() {
    if (!this.props.poll.acl.can_delete) return null

    return (
      <div className={getClassName(this.props.controls, 3)}>
        <button
          className="btn btn-default btn-block btn-sm"
          disabled={this.props.poll.isBusy}
          onClick={this.onClick}
          type="button"
        >
          {pgettext("thread poll", "Delete")}
        </button>
      </div>
    )
  }
}
