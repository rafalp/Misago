import React from "react"
import PanelMessage from "misago/components/panel-message"

export default function ({ display }) {
  if (!display) return null

  return (
    <PanelMessage
      helpText={pgettext(
        "user profile details",
        "No profile details are editable at this time."
      )}
      message={pgettext(
        "user profile details",
        "This option is currently unavailable."
      )}
    />
  )
}
