import React from "react"
import batch from "misago/utils/batch"
import Attachment from "./attachment"

export default function (props) {
  if (!isVisible(props.post)) {
    return null
  }

  return (
    <div className="post-attachments">
      {batch(props.post.attachments, 2).map((row) => {
        const key = row
          .map((a) => {
            return a ? a.id : 0
          })
          .join("_")
        return <Row key={key} row={row} />
      })}
    </div>
  )
}

export function isVisible(post) {
  return (!post.is_hidden || post.acl.can_see_hidden) && post.attachments
}

export function Row(props) {
  return (
    <div className="row">
      {props.row.map((attachment) => {
        return (
          <Attachment
            attachment={attachment}
            key={attachment ? attachment.id : 0}
          />
        )
      })}
    </div>
  )
}
