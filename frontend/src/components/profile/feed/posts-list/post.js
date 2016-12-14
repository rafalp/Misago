// jshint ignore:start
import React from 'react';
import MisagoMarkup from 'misago/components/misago-markup';

export default function(props) {
  let className = 'post post-infeed';
  if (!props.post.is_read) {
    className += ' post-new';
  }

  return (
    <li id={'post-' + props.post.id} className={className}>
      <div className="post-border">
        <div className="post-body">
          <div className="panel panel-default panel-post">
            <PostHeader post={props.post} thread={props.post.thread} />
            <PostBody content={props.post.content} />
          </div>
        </div>
      </div>
    </li>
  );
}

export function PostHeader(props) {
  return (
    <div className="panel-heading post-heading">
      <Thread {...props.thread} />
      <PostedOn post={props.post} />
      <GoTo url={props.post.url.index} />
    </div>
  );
}

export function Thread(props) {
  return (
    <a
      className="item-title"
      href={props.url}
    >
      {props.title}
    </a>
  );
}

export function PostedOn(props) {
  const tooltip = interpolate(gettext("posted %(posted_on)s"), {
    'posted_on': props.post.posted_on.format('LL, LT')
  }, true);

  const message = interpolate(gettext("posted %(posted_on)s"), {
    'posted_on': props.post.posted_on.fromNow()
  }, true);

  return (
    <a href={props.post.url.index} className="posted-on" title={tooltip}>
      {message}
    </a>
  );
}

export function GoTo(props) {
  return (
    <div className="pull-right">
      <a
        className="btn btn-default btn-sm"
        href={props.url}
      >
        {gettext("Go to post")}
      </a>
    </div>
  );
}

export function PostBody(props) {
  if (props.content) {
    return (
      <div className="panel-body">
        <MisagoMarkup markup={props.content} />
      </div>
    );
  }

  return (
    <div className="panel-body panel-body-invalid">
      <p className="lead">{gettext("This post's contents cannot be displayed.")}</p>
      <p className="text-muted">{gettext("This error is caused by invalid post content manipulation.")}</p>
    </div>
  );
}