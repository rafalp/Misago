import React from "react"
import Action from "./action"

export default function(props) {
  return (
    <Action
      execAction={makeStrikethrough}
      title={gettext("Strikethrough selection")}
      {...props}
    >
      <span className="material-icon">format_strikethrough</span>
    </Action>
  )
}

export function makeStrikethrough(selection, replace) {
  if (selection.length) {
    replace("~~" + selection + "~~")
  }
}
