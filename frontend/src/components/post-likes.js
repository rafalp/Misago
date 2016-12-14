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
    <table className="table">
      <tbody>
        {props.likes.map((like) => {
          return (
            <LikeDetails
              key={like.id}
              {...like}
            />
          );
        })}
      </tbody>
    </table>
  );
}

export function LikeDetails(props) {
  if (props.url) {
    return (
      <tr>
        <td className="col-md-6">
          <a
            className="item-title"
            href={props.url}
          >
            {props.username}
          </a>
        </td>
        <LikeDate likedOn={props.liked_on} />
      </tr>
    );
  }

  return (
    <tr>
      <td className="col-md-6">
        <strong>{props.username}</strong>
      </td>
      <LikeDate likedOn={props.liked_on} />
    </tr>
  );
}

export function LikeDate(props) {
  return (
    <td className="col-md-6">
      <abbr
        className="text-muted"
        title={props.likedOn.format('LLL')}
      >
        {props.likedOn.fromNow()}
      </abbr>
    </td>
  );
}