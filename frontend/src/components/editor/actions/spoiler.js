import React from "react"
import Action from "./action"
import isUrl from "misago/utils/is-url"

export default function(props) {
  return (
    <Action execAction={insertSpoiler} title={gettext("Insert spoiler")} {...props}>
      <span className="material-icon">not_interested</span>
    </Action>
  )
}

export function insertSpoiler(selection, replace) {
  replace("\n\n[spoiler]\n" + selection + "\n[/spoiler]\n\n")
}
