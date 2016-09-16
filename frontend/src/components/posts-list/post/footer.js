/* jshint ignore:start */
import React from 'react';
import posting from 'misago/services/posting';

export default function(props) {
  if (isVisible(props.post)) {
    return (
      <div className="panel-footer post-footer">
        <Likes {...props} />
        <Like {...props} />
        <Reply {...props} />
        <Edit {...props} />
      </div>
    );
  } else {
    return null;
  }
}

export function isVisible(post) {
  return (!post.is_hidden || post.acl.can_see_hidden) && (
    post.acl.can_reply ||
    post.acl.can_edit ||
    post.acl.can_see_likes ||
    post.acl.can_like
  );
}

export function Likes(props) {
  if (props.post.acl.can_see_likes) {
    return (
      <button type="button" className="btn btn-likes pull-left" disabled="disabled">
        Likes
      </button>
    );
  } else {
    return null;
  }
}

export function Like(props) {
  if (props.post.acl.can_like) {
    return (
      <button type="button" className="btn btn-like pull-left" disabled="disabled">
        {gettext("Like")}
      </button>
    );
  } else {
    return null;
  }
}

export class Reply extends React.Component {
  onClick = () => {
    posting.open({
      mode: 'REPLY',

      config: this.props.thread.api.editor,
      submit: this.props.thread.api.posts.index,

      context: {
        reply: this.props.post.id
      }
    });
  };

  render() {
    if (this.props.post.acl.can_reply) {
      return (
        <button type="button" className="btn btn-primary pull-right" onClick={this.onClick}>
          {gettext("Reply")}
        </button>
      );
    } else {
      return null;
    }
  }
}

export class Edit extends React.Component {
  onClick = () => {
    posting.open({
      mode: 'EDIT',

      config: this.props.post.api.editor,
      submit: this.props.post.api.index
    });
  };

  render() {
    if (this.props.post.acl.can_edit) {
      return (
        <button type="button" className="btn btn-default pull-right" onClick={this.onClick}>
          {gettext("Edit")}
        </button>
      );
    } else {
      return null;
    }
  }
}