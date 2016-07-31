/* jshint ignore:start */
import React from 'react';
import Avatar from 'misago/components/avatar';

export default function(props) {
  return (
    <li id={'post-' + props.post.id} className={getClassName(props.post)}>
      <div className="post-border">
        <div className="post-avatar">
          <PostAvatar post={props.post} />
        </div>
        <div className="post-body">
          <div className="panel panel-default panel-post">
            <PostHeader {...props} />
            <PostBody {...props} />
          </div>
        </div>
      </div>
    </li>
  );
}

export function getClassName(post) {
  if (post.is_hidden && !post.acl.can_see_hidden) {
    return 'post post-hidden';
  } else {
    return 'post';
  }
}

export function PostAvatar(props) {
  if (props.post.poster) {
    return (
      <a href={props.post.poster.absolute_url}>
        <Avatar size={100} user={props.post.poster} />
      </a>
    );
  } else {
    return <Avatar size={100} />;
  }
}

export function PostHeader(props) {
  return (
    <div className="panel-heading post-heading">
      Hello, I'm post's heading!
    </div>
  );
}

export function PostBody(props) {
  return (
    <div className="panel-body">
      Hello, I'm post's body!
    </div>
  );
}