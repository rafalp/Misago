/* jshint ignore:start */
import React from 'react';
import ReplyButton from './reply-button';
import Subscription from './subscription';
import AddParticipantModal from 'misago/components/add-participant';
import modal from 'misago/services/modal';
import posting from 'misago/services/posting';

export default function(props) {
  const hiddenSpecialOption = (
    !props.thread.acl.can_add_participants && (!props.thread.acl.can_start_poll || props.thread.poll));

  return (
    <div className="row row-toolbar row-toolbar-bottom-margin">
      <GotoMenu {...props} />
      <div className="col-xs-9 col-md-5 col-md-offset-2">
        <div className="row">
          <Spacer visible={!props.user.id} />
          <Spacer visible={hiddenSpecialOption} />
          <SubscriptionMenu {...props} />
          <StartPoll {...props} />
          <AddParticipant {...props} />
          <Reply {...props} />
        </div>
      </div>
    </div>
  );
}

export function GotoMenu(props) {
  return (
    <div className="col-xs-3 col-md-5">
      <div className="row hidden-xs hidden-sm">
        <GotoLast thread={props.thread} />
        <GotoNew thread={props.thread} />
        <GotoUnapproved thread={props.thread} />
      </div>
      <CompactOptions {...props} />
    </div>
  );
}

export function GotoNew(props) {
  if (!props.thread.is_new) return null;

  return (
    <div className="col-sm-4">
      <a
        href={props.thread.url.new_post}
        className="btn btn-default btn-block"
        title={gettext('Go to first new post')}
      >
        {gettext("New")}
      </a>
    </div>
  );
}

export function GotoUnapproved(props) {
  if (!props.thread.has_unapproved_posts || !props.thread.acl.can_approve) {
    return null;
  }

  return (
    <div className="col-sm-4">
      <a
        href={props.thread.url.unapproved_post}
        className="btn btn-default btn-block"
        title={gettext('Go to first unapproved post')}
      >
        {gettext("Unapproved")}
      </a>
    </div>
  );
}

export function GotoLast(props) {
  return (
    <div className="col-sm-4">
      <a
        href={props.thread.url.last_post}
        className="btn btn-default btn-block"
        title={gettext('Go to last post')}
      >
        {gettext("Last")}
      </a>
    </div>
  );
}

export function CompactOptions(props) {
  return (
    <div className="dropdown visible-xs-block visible-sm-block">
      <button
        aria-expanded="true"
        aria-haspopup="true"
        className="btn btn-default dropdown-toggle btn-block"
        data-toggle="dropdown"
        type="button"
      >
        <span className="material-icon">
          expand_more
        </span>
      </button>
      <ul className="dropdown-menu">
        <StartPollCompact {...props} />
        <AddParticipantCompact {...props} />
        <GotoNewCompact {...props} />
        <GotoUnapprovedCompact {...props} />
        <GotoLastCompact {...props} />
      </ul>
    </div>
  );
}

export function GotoNewCompact(props) {
  if (!props.thread.is_new) return null;

  return (
    <li>
      <a
        href={props.thread.url.new_post}
        className="btn btn-default"
      >
        {gettext("Go to first new post")}
      </a>
    </li>
  );
}

export function GotoUnapprovedCompact(props) {
  if (!props.thread.has_unapproved_posts || !props.thread.acl.can_approve) {
    return null;
  }

  return (
    <li>
      <a
        href={props.thread.url.unapproved_post}
        className="btn btn-default"
      >
        {gettext("Go to first unapproved post")}
      </a>
    </li>
  );
}

export function GotoLastCompact(props) {
  return (
    <li>
      <a
        href={props.thread.url.last_post}
        className="btn btn-default"
      >
        {gettext("Go to last post")}
      </a>
    </li>
  );
}

export function Reply(props) {
  if (!props.thread.acl.can_reply) return null;

  return (
    <div className="col-sm-4 hidden-xs">
      <ReplyButton
        className="btn btn-success btn-block"
        onClick={props.openReplyForm}
      />
    </div>
  );
}

export function SubscriptionMenu(props) {
  if (!props.user.id) return null;

  return (
    <div className="col-xs-12 col-sm-4">
      <Subscription
        className="dropdown"
        dropdownClassName="dropdown-menu dropdown-menu-right"
        {...props}
      />
    </div>
  )
}

export class StartPoll extends React.Component {
  onClick = () => {
    posting.open({
      mode: 'POLL',
      submit: this.props.thread.api.poll,

      thread: this.props.thread,
      poll: null
    });
  }

  render() {
    if (!this.props.thread.acl.can_start_poll || this.props.thread.poll) {
      return null;
    }

    return (
      <div className="col-sm-4 hidden-xs">
        <button
          className="btn btn-default btn-block"
          onClick={this.onClick}
          type="button"
        >
          <span className="material-icon">
            poll
          </span>
          {gettext("Add poll")}
        </button>
      </div>
    );
  }
}

export class StartPollCompact extends StartPoll {
  render() {
    if (!this.props.thread.acl.can_start_poll || this.props.thread.poll) {
      return null;
    }

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.onClick}
          type="button"
        >
          {gettext("Add poll")}
        </button>
      </li>
    );
  }
}

export class AddParticipant extends React.Component {
  onClick = () => {
    modal.show(
      <AddParticipantModal thread={this.props.thread} />
    );
  }

  render() {
    if (!this.props.thread.acl.can_add_participants) return null;

    return (
      <div className="col-sm-4 hidden-xs">
        <button
          className="btn btn-default btn-block"
          onClick={this.onClick}
          type="button"
        >
          <span className="material-icon">
            person_add
          </span>
          {gettext("Add participant")}
        </button>
      </div>
    );
  }
}

export class AddParticipantCompact extends AddParticipant {
  render() {
    if (!this.props.thread.acl.can_add_participants) return null;

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.onClick}
          type="button"
        >
          {gettext("Add participant")}
        </button>
      </li>
    );
  }
}

export function Spacer(props) {
  if (!props.visible) return null;

  return (
    <div className="col-sm-4 hidden-xs"/>
  );
}