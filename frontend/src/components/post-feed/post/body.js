import React from "react"
import MisagoMarkup from "misago/components/misago-markup"

export default function (props) {
  if (props.post.content) {
    return <Default {...props} />
  } else {
    return <Invalid {...props} />
  }
}

export function Default(props) {
  return (
    <div className="post-body">
      <MisagoMarkup markup={props.post.headline || props.post.content} />
    </div>
  )
}

export function Invalid(props) {
  return (
    <div className="post-body post-body-invalid">
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
