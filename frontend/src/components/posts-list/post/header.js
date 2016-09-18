/* jshint ignore:start */
import React from 'react';
import Controls from './controls';
import Select from './select';

export default function(props) {
  return (
    <div className="panel-heading post-heading">
      <Poster {...props} />
      <PosterRank {...props} />
      <PostedOn {...props} />
      <Select {...props} />
      <Controls {...props} />
      <ProtectedLabel {...props} />
      <UnreadLabel {...props} />
    </div>
  );
}

export function Poster(props) {
  if (props.post.poster) {
    return <a className="item-title" href={props.post.poster.absolute_url}>
      {props.post.poster.username}
    </a>;
  } else {
    return <strong className="item-title">{props.post.poster_name}</strong>;
  }
}

export function PosterRank(props) {
  if (props.post.poster) {
    if (!props.post.poster.rank.is_default) {
      const rankClass = 'label-' + (props.post.poster.rank.css_class || 'default');

      if (props.post.poster.rank.is_tab) {
        return <a href={props.post.poster.rank.absolute_url} className={'label ' + rankClass}>
          {props.post.poster.short_title}
        </a>;
      } else {
        return <span className={'label ' + rankClass}>
          {props.post.poster.short_title}
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

  return <a href={props.post.url.index} className="posted-on" title={tooltip}>
    {message}
  </a>;
}

export function UnreadLabel(props) {
  if (!props.post.is_read) {
    return <span className="label label-success pull-right">
      {gettext("New")}
    </span>;
  } else {
    return null;
  }
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
      className="label label-default pull-right"
      title={gettext("This post is protected and may not be edited.")}
    >
      {gettext("Protected")}
    </span>
  );
}