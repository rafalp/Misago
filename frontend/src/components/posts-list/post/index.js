/* jshint ignore:start */
import React from 'react';
import Attachments from './attachments';
import Body from './body';
import { FlagHidden, FlagUnapproved, FlagProtected } from './flags';
import Footer from './footer';
import Header from './header';
import PostSide from './post-side';

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
      <div className="panel panel-default panel-post">
        <div className="panel-body">

          <div className="row">
            <PostSide {...props} />
            <div className="col-xs-12 col-md-9">
              <Header {...props} />
              <FlagUnapproved {...props} />
              <FlagProtected {...props} />
              <FlagHidden {...props} />
              <Body {...props} />
              <Attachments {...props} />
              <Footer {...props} />
            </div>
          </div>

        </div>
      </div>
    </li>
  );
}