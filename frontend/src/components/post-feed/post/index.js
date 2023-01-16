import React from "react"
import Body from "./body"
import Header from "./header"
import PostSide from "./post-side"

export default function ({ post, poster }) {
  const user = poster || post.poster

  let className = "post"
  if (user && user.rank.css_class) {
    className += " post-" + user.rank.css_class
  }

  return (
    <li className={className} id={"post-" + post.id}>
      <div className="panel panel-default panel-post">
        <div className="panel-body">
          <div className="panel-content">
            <PostSide post={post} poster={user} />
            <Header post={post} />
            <Body post={post} />
          </div>
        </div>
      </div>
    </li>
  )
}
