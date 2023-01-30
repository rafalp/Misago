import React from "react"
import MarkupEditorButton from "./MarkupEditorButton"
import { getSelection, replaceSelection, wrapSelection } from "./operations"

const MarkupEditorToolbar = ({ disabled, element, update }) => {
  const actions = [
    {
      name: pgettext("markup editor", "Strong"),
      icon: "format_bold",
      onClick: () => {
        wrapSelection(
          getSelection(element),
          update,
          "**",
          pgettext("example markup", "Strong text")
        )
      },
    },
    {
      name: pgettext("markup editor", "Emphasis"),
      icon: "format_italic",
      onClick: () => {
        wrapSelection(
          getSelection(element),
          update,
          "*",
          pgettext("example markup", "Text with emphasis")
        )
      },
    },
    {
      name: pgettext("markup editor", "Strikethrough"),
      icon: "format_strikethrough",
      onClick: () => {
        wrapSelection(
          getSelection(element),
          update,
          "~~",
          pgettext("example markup", "Text with strikethrough")
        )
      },
    },
    {
      name: pgettext("markup editor", "Horizontal ruler"),
      icon: "remove",
      onClick: () => {
        replaceSelection(getSelection(element), update, "\n\n- - -\n\n")
      },
    },
  ]

  return (
    <div className="markup-editor-toolbar">
      {actions.map(({ name, icon, onClick }) => (
        <MarkupEditorButton
          key={icon}
          title={name}
          icon={icon}
          disabled={disabled || !element}
          onClick={onClick}
        />
      ))}
    </div>
  )
}

export default MarkupEditorToolbar
