import React from "react"

const PostingDialogError = ({ close, message }) => (
  <div className="posting-dialog-error">
    <div className="posting-dialog-error-icon">
      <span className="material-icon">error_outlined</span>
    </div>
    <div className="posting-dialog-error-detail">
      <p>{message}</p>
      <button type="button" className="btn btn-default" onClick={close}>
        {pgettext("modal", "Close")}
      </button>
    </div>
  </div>
)

export default PostingDialogError
