import React from "react"
import modal from "../../services/modal"
import isUrl from "../../utils/is-url"
import MarkupCodeModal from "./MarkupCodeModal"
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
        insertLink(element, update)
      },
    },
    {
      name: pgettext("markup editor", "Image"),
      icon: "insert_photo",
      onClick: () => {
        insertImage(element, update)
      },
    },
    {
      name: pgettext("markup editor", "Quote"),
      icon: "format_quote",
      onClick: () => {
        insertQuote(element, update)
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

const insertLink = (element, update) => {
  const selection = getSelection(element)

  let url = ""
  let label = ""

  if (selection.text.length) {
    if (isUrl(selection.text)) {
      url = selection.text.trim()
    } else {
      label = selection.text.trim()
    }
  }

  url =
    prompt(pgettext("markup editor", "Enter link address") + ":", url).trim() ||
    ""
  if (url.length === 0) return false
  label = prompt(
    pgettext("markup editor", "Enter link label (optional)").trim() + ":",
    label
  )

  if (url.length && label.length > 0) {
    replaceSelection(selection, update, "[" + label + "](" + url + ")")
  }
}

const insertImage = (element, update) => {
  const selection = getSelection(element)

  let url = ""
  let label = ""

  if (selection.text.length) {
    if (isUrl(selection.text)) {
      url = selection.text.trim()
    } else {
      label = selection.text.trim()
    }
  }

  url =
    prompt(
      pgettext("markup editor", "Enter a link to image") + ":",
      url
    ).trim() || ""
  if (url.length === 0) return false
  label = prompt(
    pgettext("markup editor", "Enter image label (optional)").trim() + ":",
    label
  )

  if (url.length) {
    if (label.length > 0) {
      replaceSelection(selection, update, "![" + label + "](" + url + ")")
    } else {
      replaceSelection(selection, update, "!(" + url + ")")
    }
  }
}

const insertQuote = (element, update) => {
  const selection = getSelection(element)

  const title = prompt(
    pgettext("markup editor", "Enter quote autor, prefix usernames with @") +
      ":"
  ).trim()

  const prefix = selection.prefix.trim().length ? "\n\n" : ""

  if (title) {
    wrapSelection(
      selection,
      update,
      prefix + '[quote="' + title + '"]\n',
      "\n[/quote]\n\n",
      pgettext("markup editor", "Quote text")
    )
  } else {
    wrapSelection(
      selection,
      update,
      prefix + "[quote]\n",
      "\n[/quote]\n\n",
      pgettext("markup editor", "Quote text")
    )
  }
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

const insertCode = (element, update) => {
  const selection = getSelection(element)
  const prefix = selection.prefix.trim().length ? "\n\n" : ""
  const syntax =
    prompt(
      pgettext(
        "markup editor",
        "Enter name of syntax of your code (optional)"
      ).trim() + ":"
    ) || ""

  wrapSelection(
    selection,
    update,
    prefix + "```" + syntax + "\n",
    "\n```\n\n",
    pgettext("markup editor", "Spoiler text")
  )
}

export default MarkupEditorToolbar
