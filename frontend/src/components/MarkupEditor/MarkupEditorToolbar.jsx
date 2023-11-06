import React from "react"
import misago from "../../"
import modal from "../../services/modal"
import MarkupCodeModal from "./MarkupCodeModal"
import MarkupFormattingHelpModal from "./MarkupFormattingHelpModal"
import MarkupImageModal from "./MarkupImageModal"
import MarkupLinkModal from "./MarkupLinkModal"
import MarkupQuoteModal from "./MarkupQuoteModal"
import MarkupEditorButton from "./MarkupEditorButton"
import { getSelection, replaceSelection, wrapSelection } from "./operations"
import uploadFile from "./uploadFile"

const MarkupEditorToolbar = ({
  disabled,
  element,
  update,
  updateAttachments,
}) => {
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
  ]

  if (misago.get("user").acl.max_attachment_size) {
    actions.push({
      name: pgettext("markup editor", "Upload file"),
      icon: "file_upload",
      onClick: () => uploadFiles(updateAttachments),
    })
  }

  return (
    <div className="markup-editor-toolbar">
      <div className="markup-editor-toolbar-left">
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
      <div className="markup-editor-toolbar-right">
        <div className="markup-editor-controls-dropdown">
          <button
            type="button"
            className="btn btn-markup-editor dropdown-toggle"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
            disabled={disabled || !element}
          >
            <span className="material-icon">more_vert</span>
          </button>
          <ul className="dropdown-menu dropdown-menu-right stick-to-bottom">
            {actions.map(({ name, icon, onClick }) => (
              <li key={icon}>
                <button
                  type="button"
                  className="btn-link"
                  disabled={disabled || !element}
                  onClick={onClick}
                >
                  <span className="material-icon">{icon}</span>
                  {name}
                </button>
              </li>
            ))}
          </ul>
        </div>
        <MarkupEditorButton
          title={pgettext("markup editor", "Open formatting help")}
          icon="help_outline"
          onClick={() => {
            modal.show(<MarkupFormattingHelpModal />)
          }}
        />
      </div>
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

const uploadFiles = (setState) => {
  const input = document.createElement("input")
  input.type = "file"
  input.multiple = "multiple"

  input.addEventListener("change", function () {
    for (let i = 0; i < input.files.length; i++) {
      uploadFile(input.files[i], setState)
    }
  })

  input.click()
}

export default MarkupEditorToolbar
