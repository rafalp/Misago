import React from "react"
import Attachments from "./attachments"
import Body from "./body"
import {
  FlagBestAnswer,
  FlagHidden,
  FlagUnapproved,
  FlagProtected,
} from "./flags"
import Footer from "./footer"
import Header from "./header"
import PostSide from "./post-side"

export default function (props) {
  let className = "post"
  if (props.post.isDeleted) {
    className = "hide"
  } else if (props.post.is_hidden && !props.post.acl.can_see_hidden) {
    className = "post post-hidden"
  }

  if (props.post.poster && props.post.poster.rank.css_class) {
    className += " post-" + props.post.poster.rank.css_class
  }

  if (!props.post.is_read) {
    className += " post-new"
  }

  return (
    <li id={"post-" + props.post.id} className={className}>
      <div className="panel panel-default panel-post">
        <div className="panel-body">
          <PostSide {...props} />
          <div className="panel-content">
            <Header {...props} />
            <FlagBestAnswer {...props} />
            <FlagUnapproved {...props} />
            <FlagProtected {...props} />
            <FlagHidden {...props} />
            <Body {...props} />
            <Attachments {...props} />
            <Footer {...props} />
          </div>
        </div>
      </div>
    </li>
  )
}
