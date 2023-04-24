import React from "react"
import { connect } from "react-redux"
import { close } from "../../reducers/overlay"

export function OverlayHeader({ branding, children, dispatch }) {
  return (
    <div className="overlay-header">
      {!!branding.logo && (
        <div className="overlay-header-branding">
          <a href={branding.url}>
            <img src={branding.logo} title={branding.text} />
          </a>
        </div>
      )}
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

function select() {
  const settings = misago.get("SETTINGS")

  return {
    branding: {
      logo: settings.logo_small,
      text: settings.logo_text,
      url: misago.get("MISAGO_PATH"),
    },
  }
}

const OverlayHeaderConnected = connect(select)(OverlayHeader)

export default OverlayHeaderConnected
