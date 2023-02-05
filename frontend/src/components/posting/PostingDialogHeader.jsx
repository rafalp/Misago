import React from "react"

const PostingDialogHeader = ({
  children,
  close,
  fullscreen,
  minimize,
  minimized,
  fullscreenEnter,
  fullscreenExit,
  open,
}) => (
  <div className="posting-dialog-header">
    <div className="posting-dialog-caption">{children}</div>
    {minimized ? (
      <button
        className="btn btn-posting-dialog"
        title={pgettext("dialog", "Open")}
        type="button"
        onClick={open}
      >
        <span className="material-icon">expand_less</span>
      </button>
    ) : (
      <button
        className="btn btn-posting-dialog"
        title={pgettext("dialog", "Minimize")}
        type="button"
        onClick={minimize}
      >
        <span className="material-icon">expand_more</span>
      </button>
    )}
    {fullscreen ? (
      <button
        className="btn btn-posting-dialog hidden-xs"
        title={pgettext("dialog", "Exit the fullscreen mode")}
        type="button"
        onClick={fullscreenExit}
      >
        <span className="material-icon">fullscreen_exit</span>
      </button>
    ) : (
      <button
        className="btn btn-posting-dialog hidden-xs"
        title={pgettext("dialog", "Enter the fullscreen mode")}
        type="button"
        onClick={fullscreenEnter}
      >
        <span className="material-icon">fullscreen</span>
      </button>
    )}
    <button
      className="btn btn-posting-dialog"
      title={pgettext("dialog", "Cancel")}
      type="button"
      onClick={close}
    >
      <span className="material-icon">close</span>
    </button>
  </div>
)

export default PostingDialogHeader
