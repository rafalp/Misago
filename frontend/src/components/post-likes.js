// jshint ignore:start
import React from 'react';
import moment from 'moment';
import Message from 'misago/components/modal-message';
import Loader from 'misago/components/modal-loader';
import ajax from 'misago/services/ajax';


export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isReady: false,

      error: null,
      likes: []
    };
  }

  componentDidMount() {
    ajax.get(this.props.post.api.likes).then((data) => {
      this.setState({
        isReady: true,
        likes: data.map(hydrateLike)
      });
    }, (rejection) => {
      this.setState({
        isReady: true,
        error: rejection.detail
      });
    });
  };

  render() {
    if (this.state.error) {
      return (
        <ModalDialog className="modal-message">
          <Message
            message={this.state.error}
          />
        </ModalDialog>
      );
    } else if (this.state.isReady) {
      if (this.state.likes.length) {
        return (
          <ModalDialog>
            <LikesList
              likes={this.state.likes}
            />
          </ModalDialog>
        );
      }

      return (
        <ModalDialog className="modal-message">
          <Message
            message={gettext("No users have liked this post.")}
          />
        </ModalDialog>
      );
    }

    return (
      <ModalDialog>
        <Loader />
      </ModalDialog>
    );
  }
}

export function hydrateLike(data) {
  return Object.assign({}, data, {
    liked_on: moment(data.liked_on)
  });
}

export function ModalDialog(props) {
  return (
    <div
      className={"modal-dialog modal-sm " + (props.className || '')}
      role="document"
    >
      <div className="modal-content">
        <div className="modal-header">
          <button
            aria-label={gettext("Close")}
            className="close"
            data-dismiss="modal"
            type="button"
          >
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 className="modal-title">{gettext("Post Likes")}</h4>
        </div>
        {props.children}
      </div>
    </div>
  )
}

export function LikesList(props) {
  return (
    <div className="modal-body modal-post-likers">
      <ul className="list-unstyled">
        {props.likes.map((like) => {
          return (
            <LikeDetails
              key={like.id}
              {...like}
            />
          );
        })}
      </ul>
    </div>
  );
}

export function LikeDetails(props) {
  if (props.url) {
    return (
      <li>
        <a
          className="item-title"
          href={props.url}
        >
          {props.username}
        </a>
        {' '}
        <LikeDate likedOn={props.liked_on} />
      </li>
    );
  }

  return (
    <li>
      <strong>{props.username}</strong>
      {' '}
      <LikeDate likedOn={props.liked_on} />
    </li>
  );
}

export function LikeDate(props) {
  return (
    <abbr
      className="text-muted"
      title={props.likedOn.format('LLL')}
    >
      {props.likedOn.fromNow()}
    </abbr>
  );
}