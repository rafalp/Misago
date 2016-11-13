// jshint ignore:start
import React from 'react';
import * as poll from 'misago/reducers/poll';
import * as thread from 'misago/reducers/thread';
import ajax from 'misago/services/ajax';
import posting from 'misago/services/posting';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';

export default function(props) {
  if (!isVisible(props.isPollOver, props.poll.acl, props.poll)) return null;

  return (
    <ul className="list-unstyled list-inline poll-options">
      <ChangeVote
        isPollOver={props.isPollOver}
        poll={props.poll}
        showVoting={props.showVoting}
      />
      <SeeVotes poll={props.poll} />
      <Edit
        poll={props.poll}
        thread={props.thread}
      />
      <Delete poll={props.poll} />
    </ul>
  );
}

export function isVisible(isPollOver, acl, poll) {
  return (
    poll.is_public ||
    acl.can_delete ||
    acl.can_edit ||
    acl.can_see_votes ||
    (acl.can_vote && !isPollOver && (!poll.hasSelectedChoices || poll.allow_revotes))
  );
}

export function ChangeVote(props) {
  const canVote = props.poll.acl.can_vote;
  const canChangeVote = !props.poll.hasSelectedChoices || props.poll.allow_revotes;

  if (!(canVote && canChangeVote)) return null;

  return (
    <li>
      <button
        className="btn btn-default"
        disabled={props.poll.isBusy}
        onClick={props.showVoting}
      >
        {gettext("Vote")}
      </button>
    </li>
  );
}

export class SeeVotes extends React.Component {
  onClick = () => {
    alert("TODO!");
  };

  render() {
    const seeVotes = this.props.poll.is_public || this.props.poll.acl.can_see_votes;
    if (!seeVotes) return null;

    return (
      <li>
        <button
          className="btn btn-default"
          disabled={this.props.poll.isBusy}
          onClick={this.onClick}
        >
          {gettext("See votes")}
        </button>
      </li>
    );
  }
}

export class Edit extends React.Component {
  onClick = () => {
    posting.open({
      thread: this.props.thread,
      poll: this.props.poll,
      config: {
        mode: 'POLL'
      }
    });
  };

  render() {
    if (!this.props.poll.acl.can_edit) return null;

    return (
      <li>
        <button
          className="btn btn-default"
          disabled={this.props.poll.isBusy}
          onClick={this.onClick}
        >
          {gettext("Edit")}
        </button>
      </li>
    );
  }
}

export class Delete extends React.Component {
  onClick = () => {
    const deletePoll = confirm(gettext("Are you sure you want to delete this poll? This action is not reversible."));
    if (deletePoll) {
      store.dispatch(poll.busy());

      ajax.delete(this.props.poll.api.index).then(
        this.handleSuccess, this.handleError);
    }
  };

  handleSuccess = (newThreadAcl) => {
    snackbar.success("Poll has been deleted");
    store.dispatch(poll.remove());
    store.dispatch(thread.updateAcl(newThreadAcl));
  };

  handleError = (rejection) => {
    snackbar.apiError(rejection);
    store.dispatch(poll.release());
  };

  render() {
    if (!this.props.poll.acl.can_delete) return null;

    return (
      <li>
        <button
          className="btn btn-default"
          disabled={this.props.poll.isBusy}
          onClick={this.onClick}
        >
          {gettext("Delete")}
        </button>
      </li>
    );
  }
}