/* jshint ignore:start */
import React from 'react';
import Attachments from './attachments';
import Body from './body';
import { FlagHidden, FlagUnapproved, FlagProtected } from './flags';
import Footer from './footer';
import Header from './header';
import PosterAvatar from './poster-avatar';

export default function(props) {
  let className = 'post';
  if (props.post.isDeleted) {
    className = 'hide';
  } else if (props.post.is_hidden && !props.post.acl.can_see_hidden) {
    className = 'post post-hidden';
  }

  if (!props.post.is_read) {
    className += ' post-new';
  }

  return (
    <li id={'post-' + props.post.id} className={className}>
      <div className="post-border">
        <div className="post-avatar post-avatar-lg">
          <PosterAvatar post={props.post} />
        </div>
        <div className="post-body">
          <div className="panel panel-default panel-post">
            <Header {...props} />
            <FlagHidden {...props} />
            <FlagUnapproved {...props} />
            <FlagProtected {...props} />
            <Body {...props} />
            <Attachments {...props} />
            <Footer {...props} />
          </div>
        </div>
      </div>
    </li>
  );
}
