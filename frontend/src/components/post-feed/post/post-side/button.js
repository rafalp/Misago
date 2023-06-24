import React from "react"

export default function ({ post }) {
  return (
    <a className="btn btn-default btn-icon pull-right" href={post.url.index}>
      <span className="btn-text-left hidden-xs">
        {pgettext("go to post link", "See post")}
      </span>
      <span className="material-icon">chevron_right</span>
    </a>
  )
}
