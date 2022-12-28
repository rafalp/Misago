import React from "react"
import Action from "./action"

export default function (props) {
  return (
    <Action
      execAction={insertHr}
      title={gettext("Insert horizontal ruler")}
      {...props}
    >
      <span className="material-icon">remove</span>
    </Action>
  )
}

export function insertHr(selection, replace) {
  replace("\n\n- - - - -\n\n")
}
