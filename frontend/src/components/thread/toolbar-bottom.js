/* jshint ignore:start */
import React from 'react';
import { Pager, More } from './paginator';
import PostsModeration from './moderation/posts';
import ReplyButton from './reply-button';
import SubscriptionSwitch from './subscription';

export default function(props) {
  return (
    <div className="row row-toolbar">
      <div className="col-xs-12 text-center visible-xs-block">
        <More more={props.posts.more} />
        <div className="clearfix visible-xs-block" />
      </div>
      <div className="col-md-3">
        <Pager {...props} />
      </div>
      <div className="col-md-4 hidden-xs">
        <More more={props.posts.more} />
      </div>
      <Options visible={!!props.user.id}>
        <div className="clearfix visible-xs-block" />
        <div className="row">
          <Spacer {...props} />
          <Moderation {...props} />
          <Subscription {...props} />
          <Reply
            thread={props.thread}
            onClick={props.openReplyForm}
          />
        </div>
      </Options>
    </div>
  );
}

export function Options(props) {
  if (!props.visible) return null;

  return (
    <div className="col-md-5">
      {props.children}
    </div>
  )
}

export function Moderation(props) {
  if (!props.user.id) return null;

  return (
    <div className="col-md-4 hidden-xs">
      <PostsModeration {...props} />
    </div>
  )
}


export function Subscription(props) {
  let xsClass = "col-xs-6";
  if (!props.thread.acl.can_reply) {
    xsClass = 'col-xs-12';
  }

  return (
    <div className={xsClass + " col-md-4"}>
      <SubscriptionSwitch
        btnClassName="btn-block"
        className="dropup"
        {...props}
      />
    </div>
  );
}

export function Reply(props) {
  if (!props.thread.acl.can_reply) return null;

  return (
    <div className="col-xs-6 col-md-4">
      <ReplyButton
        className="btn btn-success btn-block"
        onClick={props.onClick}
      />
    </div>
  );
}

export function Spacer(props) {
  if (props.thread.acl.can_reply) return null;

  return (
    <div className="hidden-xs col-md-4"></div>
  );
}