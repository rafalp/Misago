import React from "react"
import { connect } from "react-redux"
import { close } from "../../reducers/overlay"

export function OverlayHeader({ children, dispatch }) {
  return (
    <div className="overlay-header">
      <div className="overlay-header-caption">{children}</div>
      <button
        className="btn btn-overlay-close"
        title={pgettext("modal", "Close")}
        type="button"
        onClick={() => dispatch(close())}
      >
        <span className="material-icon">close</span>
      </button>
    </div>
  )
}

const OverlayHeaderConnected = connect()(OverlayHeader)

export default OverlayHeaderConnected
