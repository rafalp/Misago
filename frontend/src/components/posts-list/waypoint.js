/* jshint ignore:start */
import React from 'react';
import * as post from 'misago/reducers/post';
import * as thread from 'misago/reducers/thread';
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';

export default class extends React.Component {
  /*
  Super naive and de-facto placeholder implementation for reading posts on scroll
  */
  componentDidMount() {
    if(this.props.post.is_read) return; // don't register read tracker

    $(this.documentNode).waypoint({
      handler: (direction) => {
        if (direction !== 'down' || this.props.post.is_read) return;

        // after 1500ms run flag post as read logic
        window.setTimeout(() => {
          // check if post's bottom edge is still in viewport
          const boundingClientRect = this.documentNode.getBoundingClientRect();
          const offsetBottom = boundingClientRect.height + boundingClientRect.top;
          const clientHeight = document.documentElement.clientHeight;

          if (offsetBottom < 5) return; // scrolled past the post
          if (offsetBottom > clientHeight) return; // scrolled back up

          // mark post as read
          store.dispatch(post.patch(this.props.post, {
            is_read: true
          }));

          // call API to let it know we have unread post
          ajax.post(this.props.post.api.read).then(
            (data) => {
              store.dispatch(thread.update(this.props.thread, {
                is_read: data.thread_is_read
              }));
            },
            (rejection) => {
              snackbar.apiError(rejection);
            }
          );
        }, 1000);
      },
      offset: 'bottom-in-view'
    });
  }

  render() {
    return (
      <div className={this.props.className} ref={(node) => { this.documentNode = node; }}>
        {this.props.children}
      </div>
    );
  }
}