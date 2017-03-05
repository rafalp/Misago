/* jshint ignore:start */
import React from 'react';
import Controls from './controls';
import Select from './select';
import {StatusIcon, getStatusClassName, getStatusDescription} from 'misago/components/user-status';
import PostChangelog from 'misago/components/post-changelog';
import PosterAvatar from './poster-avatar';
import modal from 'misago/services/modal';

export default function(props) {
  return (
    <div className="panel-heading post-heading">
      <div className="post-avatar-sm visible-xs-block">
        <PosterAvatar
          post={props.post}
          size={50}
        />
      </div>
      <div className="post-heading-container">
        <PosterStatus {...props} />
        <Poster {...props} />
        <PosterRank {...props} />
        <PostedOn {...props} />
        <PostedOnCompact {...props} />
        <EditedCompact {...props} />
        <UnreadCompact {...props} />
        <Select {...props} />
        <Controls {...props} />
        <PostEdits {...props} />
        <ProtectedLabel {...props} />
        <UnreadLabel {...props} />
      </div>
    </div>
  );
}

export function PosterStatus(props) {
  if (!props.post.poster) {
    return null;
  }

  return (
    <div
      className={getStatusClassName(props.post.poster.status)}
      title={getStatusDescription(props.post.poster, props.post.poster.status)}
    >
      <StatusIcon
        status={props.post.poster.status}
        user={props.post.poster}
      />
    </div>
  );
}

export function Poster(props) {
  if (props.post.poster) {
    return (
      <a className="item-title" href={props.post.poster.absolute_url}>
        {props.post.poster.username}
      </a>
    );
  } else {
    return (
      <strong className="item-title">{props.post.poster_name}</strong>
    );
  }
}

export function PosterRank(props) {
  if (props.post.poster) {
    const { poster }  = props.post;
    const { rank } = poster;

    if (!rank.is_default) {
      const rankClass = 'label-' + (rank.css_class || 'default');

      if (rank.is_tab) {
        return <a href={rank.absolute_url} className={'label ' + rankClass}>
          {poster.title || rank.title || rank.name}
        </a>;
      } else {
        return <span className={'label ' + rankClass}>
          {poster.title || rank.title || rank.name}
        </span>;
      }
    } else {
      return null; // we don't display default ranks
    }
  } else {
    return <span className="rank-name item-title">
      {gettext("Unregistered")}
    </span>;
  }
}

export function PostedOn(props) {
  const tooltip = interpolate(gettext("posted %(posted_on)s"), {
    'posted_on': props.post.posted_on.format('LL, LT')
  }, true);

  const message = interpolate(gettext("posted %(posted_on)s"), {
    'posted_on': props.post.posted_on.fromNow()
  }, true);

  return (
    <a
      href={props.post.url.index}
      className="posted-on hidden-xs"
      title={tooltip}
    >
      {message}
    </a>
  );
}

export function PostedOnCompact(props) {
  return (
    <span className="posted-on-compact visible-xs-inline-block">
      {props.post.posted_on.fromNow()}
    </span>
  );
}

export function EditedCompact(props) {
  const isHidden = props.post.is_hidden && !props.post.acl.can_see_hidden;
  const isUnedited = props.post.edits === 0;
  if (isHidden || isUnedited) return null;

  return (
    <span className="edited-compact visible-xs-inline-block">
      {gettext("edited")}
    </span>
  );
}

export function UnreadCompact(props) {
  if (props.post.is_read) return null;

  return (
    <span className="unread-compact text-warning visible-xs-inline-block">
      {gettext("new")}
    </span>
  );
}

export class PostEdits extends React.Component {
  onClick = () => {
    modal.show(
      <PostChangelog post={this.props.post} />
    )
  };

  render() {
    const isHidden = this.props.post.is_hidden && !this.props.post.acl.can_see_hidden;
    const isUnedited = this.props.post.edits === 0;
    if (isHidden || isUnedited) return null;

    const message = ngettext(
      "This post was edited %(edits)s time.",
      "This post was edited %(edits)s times.",
      this.props.post.edits
    );

    const title = interpolate(message, {
      'edits': this.props.post.edits
    }, true);

    return (
      <button
        className="btn btn-default btn-sm pull-right hidden-xs"
        onClick={this.onClick}
        title={title}
        type="button"
      >
        <span className="material-icon">
          edit
        </span>
        {this.props.post.edits}
      </button>
    )
  }
}

export function UnreadLabel(props) {
  if (props.post.is_read) return null;

  return (
    <span className="label label-warning pull-right hidden-xs">
      {gettext("New")}
    </span>
  );
}

export function ProtectedLabel(props) {
  const postAuthor = props.post.poster && props.post.poster.id === props.user.id;
  const hasAcl = props.post.acl.can_protect;
  const isVisible = props.user.id && props.post.is_protected && (postAuthor || hasAcl);

  if (!isVisible) {
    return null;
  }

  return (
    <span
      className="label label-default pull-right hidden-xs"
      title={gettext("This post is protected and may not be edited.")}
    >
      {gettext("Protected")}
    </span>
  );
}