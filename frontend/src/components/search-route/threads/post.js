import React from "react"
import PostFooter from "./footer"
import MisagoMarkup from "misago/components/misago-markup"

export default function (props) {
  return (
    <li id={"post-" + props.post.id} className="post post-infeed">
      <div className="post-border">
        <div className="post-body">
          <div className="panel panel-default panel-post">
            <PostBody content={props.post.headline || props.post.content} />
            <PostFooter
              category={props.post.category}
              post={props.post}
              thread={props.post.thread}
            />
          </div>
        </div>
      </div>
    </li>
  )
}

export function PostBody(props) {
  if (props.content) {
    return (
      <div className="panel-body">
        <MisagoMarkup markup={props.content} />
      </div>
    )
  }

  return (
    <div className="panel-body panel-body-invalid">
      <p className="lead">
        {pgettext(
          "post body invalid",
          "This post's contents cannot be displayed."
        )}
      </p>
      <p className="text-muted">
        {pgettext(
          "post body invalid",
          "This error is caused by invalid post content manipulation."
        )}
      </p>
    </div>
  )
}
