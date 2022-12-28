import React from "react"
import * as posts from "misago/reducers/posts"
import store from "misago/services/store"

export default class extends React.Component {
  onClick = () => {
    if (this.props.post.isSelected) {
      store.dispatch(posts.deselect(this.props.post))
    } else {
      store.dispatch(posts.select(this.props.post))
    }
  }

  render() {
    if (
      !(this.props.thread.acl.can_merge_posts || isVisible(this.props.post.acl))
    ) {
      return null
    }

    return (
      <div className="pull-right">
        <button
          className="btn btn-default btn-icon"
          onClick={this.onClick}
          type="button"
        >
          <span className="material-icon">
            {this.props.post.isSelected
              ? "check_box"
              : "check_box_outline_blank"}
          </span>
        </button>
      </div>
    )
  }
}

export function isVisible(acl) {
  return (
    acl.can_approve ||
    acl.can_hide ||
    acl.can_protect ||
    acl.can_unhide ||
    acl.can_delete ||
    acl.can_move
  )
}
