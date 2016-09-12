/* jshint ignore:start */
import React from 'react';
import Avatar from 'misago/components/avatar';
import Body from './body';
import { FlagHidden, FlagUnapproved } from './flags';
import Footer from './footer';
import Header from './header';

export default function(props) {
  let className = 'post';
  if (props.post.isDeleted) {
    className = 'hide';
  } else if (props.post.is_hidden && !props.post.acl.can_see_hidden) {
    className = 'post post-hidden';
  }

  return (
    <li id={'post-' + props.post.id} className={className}>
      <div className="post-border">
        <div className="post-avatar">
          <PosterAvatar post={props.post} />
        </div>
        <div className="post-body">
          <div className="panel panel-default panel-post">
            <Header {...props} />
            <FlagHidden {...props} />
            <FlagUnapproved {...props} />
            <Body {...props} />
            <Footer {...props} />
          </div>
        </div>
      </div>
    </li>
  );
}

export function PosterAvatar(props) {
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
