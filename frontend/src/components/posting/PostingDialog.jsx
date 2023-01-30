import React from "react"
import classnames from "classnames"

const PostingDialog = ({ children, fullscreen, minimized }) => (
  <div
    className={classnames("posting-dialog", {
      "posting-dialog-minimized": minimized,
      "posting-dialog-fullscreen": fullscreen && !minimized,
    })}
  >
    <div className="posting-dialog-container">{children}</div>
  </div>
)

export default PostingDialog
