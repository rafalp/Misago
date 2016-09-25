/* jshint ignore:start */
import React from 'react';
import * as post from 'misago/reducers/post';
import ajax from 'misago/services/ajax';
import store from 'misago/services/store';

export default class extends React.Component {
  /*
  Super naive and de-facto placeholder implementation for reading posts on scroll
  */
  componentDidMount() {
    if(this.props.post.is_read) {
      return; // don't register read tracker
    }

    $('#post-' + this.props.post.id).waypoint({
      handler: (direction) => {
        if (direction !== 'down' || this.props.post.is_read) {
          return;
        }

        // after 1500ms flag post as read
        window.setTimeout(() => {
          store.dispatch(post.patch(this.props.post, {
            is_read: true
          }));

          ajax.post(this.props.post.api.read);
        }, 1000);
      },
      offset: 'bottom-in-view'
    });
  }

  render() {
    return (
      <div className={this.props.className}>
        <div style={{borderColor: '#f00'}}>
          {this.props.children}
        </div>
      </div>
    );
  }
}