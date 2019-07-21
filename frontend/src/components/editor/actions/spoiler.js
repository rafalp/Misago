import React from "react"
import Action from "./action"
import isUrl from "misago/utils/is-url"

export default function(props) {
  return (
    <Action execAction={insertQuote} title={gettext("Insert spoiler")} {...props}>
      <span className="material-icon">not_interested</span>
    </Action>
  )
}

export function insertQuote(selection, replace) {
  let title = $.trim(
    prompt(gettext("Enter spoiler title (optional)") + ":", title)
  )

  if (title) {
    replace('\n\n[spoiler="' + title + '"]\n' + selection + "\n[/spoiler]\n\n")
  } else {
    replace("\n\n[spoiler]\n" + selection + "\n[/spoiler]\n\n")
  }
}
