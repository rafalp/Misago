/* jshint ignore:start */
import React from 'react';
import * as actions from './controls/actions';
import LikesModal from 'misago/components/post-likes';
import modal from 'misago/services/modal';
import posting from 'misago/services/posting';

export default function(props) {
  if (isVisible(props.post)) {
    return (
      <div className="panel-footer post-footer">
        <Like {...props} />
        <Likes
          lastLikes={props.post.last_likes}
          likes={props.post.likes}
          {...props}
        />
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

export class Like extends React.Component {
  onClick = () => {
    if (this.props.post.is_liked) {
      actions.unlike(this.props);
    } else {
      actions.like(this.props);
    }
  };

  render() {
    if (!this.props.post.acl.can_like) return null;

    return (
      <button
        className="btn btn-default pull-left"
        disabled={this.props.post.isBusy}
        onClick={this.onClick}
        type="button"
      >
        {this.props.post.is_liked ? gettext("Unlike") : gettext("Like")}
      </button>
    );
  }
}

export class Likes extends React.Component {
  onClick = () => {
    modal.show(
      <LikesModal
        post={this.props.post}
      />
    );
  };

  render() {
    if (!this.props.post.acl.can_see_likes || !this.props.post.last_likes) return null;

    if (this.props.post.acl.can_see_likes === 2) {
      return (
        <button
          className="btn btn-link pull-left"
          onClick={this.onClick}
          type="button"
        >
          {getLikesMessage(this.props.likes, this.props.lastLikes)}
        </button>
      );
    }

    return (
      <p className="pull-left">
        {getLikesMessage(this.props.likes, this.props.lastLikes)}
      </p>
    );
  }
}

export function getLikesMessage(likes, users) {
  const usernames = users.slice(0, 3).map((u) => u.username);

  if (usernames.length == 1) {
    return interpolate(gettext("%(user)s likes this."), {
      user: usernames[0]
    }, true);
  }

  const hiddenLikes = likes - usernames.length;

  const otherUsers = usernames.slice(0, -1).join(', ');
  const lastUser = usernames.slice(-1)[0];

  const usernamesList = interpolate(gettext("%(users)s and %(last_user)s"), {
    users: otherUsers,
    last_user: lastUser
  }, true);

  if (hiddenLikes === 0) {
    return interpolate(gettext("%(users)s like this."), {
      users: usernamesList
    }, true);
  }

  const message = ngettext(
    "%(users)s and %(likes)s other user like this.",
    "%(users)s and %(likes)s other users like this.",
    hiddenLikes);

  return interpolate(message, {
    users: usernamesList,
    likes: hiddenLikes
  }, true);
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