import React from "react"
import modal from "../../services/modal"
import MarkupCodeModal from "./MarkupCodeModal"
import MarkupImageModal from "./MarkupImageModal"
import MarkupLinkModal from "./MarkupLinkModal"
import MarkupQuoteModal from "./MarkupQuoteModal"
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
    {
      name: pgettext("markup editor", "Link"),
      icon: "insert_link",
      onClick: () => {
        const selection = getSelection(element)
        modal.show(
          <MarkupLinkModal
            selection={selection}
            element={element}
            update={update}
          />
        )
      },
    },
    {
      name: pgettext("markup editor", "Image"),
      icon: "insert_photo",
      onClick: () => {
        const selection = getSelection(element)
        modal.show(
          <MarkupImageModal
            selection={selection}
            element={element}
            update={update}
          />
        )
      },
    },
    {
      name: pgettext("markup editor", "Quote"),
      icon: "format_quote",
      onClick: () => {
        const selection = getSelection(element)
        modal.show(
          <MarkupQuoteModal
            selection={selection}
            element={element}
            update={update}
          />
        )
      },
    },
    {
      name: pgettext("markup editor", "Spoiler"),
      icon: "visibility_off",
      onClick: () => {
        insertSpoiler(element, update)
      },
    },
    {
      name: pgettext("markup editor", "Code"),
      icon: "code",
      onClick: () => {
        const selection = getSelection(element)
        modal.show(
          <MarkupCodeModal
            selection={selection}
            element={element}
            update={update}
          />
        )
      },
    },
    {
      name: pgettext("markup editor", "Upload file"),
      icon: "file_upload",
      onClick: () => {
        console.log("TODO")
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

const insertSpoiler = (element, update) => {
  const selection = getSelection(element)
  const prefix = selection.prefix.trim().length ? "\n\n" : ""

  wrapSelection(
    selection,
    update,
    prefix + "[spoiler]\n",
    "\n[/spoiler]\n\n",
    pgettext("markup editor", "Spoiler text")
  )
}

export default MarkupEditorToolbar
