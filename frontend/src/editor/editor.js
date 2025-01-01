import htmx from "htmx.org"
import {
  MarkupEditorCodeModal,
  MarkupEditorImageModal,
  MarkupEditorLinkModal,
  MarkupEditorQuoteModal,
} from "./modals"

class MarkupEditor {
  constructor() {
    this.actions = {}

    this.codeModal = new MarkupEditorCodeModal()
    this.linkModal = new MarkupEditorLinkModal()
    this.imageModal = new MarkupEditorImageModal()
    this.quoteModal = new MarkupEditorQuoteModal()
  }

  setAction = (name, init) => {
    this.actions[name] = init
  }

  activate = (element) => {
    if (element.getAttribute("misago-editor-active") !== "true") {
      this.setEditorActive(element)
      this.setEditorFocus(element)
      this.setEditorActions(element)
    }
  }

  setEditorActive(element) {
    element.setAttribute("misago-editor-active", "true")
  }

  setEditorFocus(element) {
    element.addEventListener("focusin", () => {
      element.classList.add("markup-editor-focused")
    })

    element.addEventListener("focusout", () => {
      element.classList.remove("markup-editor-focused")
    })
  }

  setEditorActions(element) {
    const input = element.querySelector("textarea")

    element.querySelectorAll("[misago-editor-action]").forEach((control) => {
      const actionName = control.getAttribute("misago-editor-action")
      control.addEventListener("click", (event) => {
        event.preventDefault()

        const action = this.actions[actionName]
        if (action) {
          action({
            input,
            target: event.target,
            editor: this,
            selection: new MarkupEditorSelection(input),
          })
        } else {
          console.warn("Undefined editor action: " + actionName)
        }
      })
    })
  }

  showCodeModal(selection) {
    this.codeModal.show(selection)
  }

  showLinkModal(selection) {
    this.linkModal.show(selection)
  }

  showImageModal(selection) {
    this.imageModal.show(selection)
  }

  showQuoteModal(selection) {
    this.quoteModal.show(selection)
  }
}

class MarkupEditorSelection {
  constructor(input) {
    this.input = input
    this._range = this._getRange()
  }

  get() {
    return this._range
  }

  prefix() {
    return this._range.prefix
  }

  suffix() {
    return this._range.suffix
  }

  zero() {
    return this._range.length === 0
  }

  empty() {
    return this._range.text.trim().length === 0
  }

  text() {
    return this._range.text
  }

  wrap(prefix, suffix) {
    let value = this._range.prefix
    value += prefix + this._range.text + suffix
    value += this._range.suffix

    this.input.value = value

    this._range.start += prefix.length
    this._range.end += prefix.length
    this._range.length = this._range.end - this._range.start

    this.refocus()
  }

  replace(text, options) {
    const value = this._range.prefix + text + this._range.suffix
    this.input.value = value

    if (options && options.start) {
      this._range.start += options.start
    }

    this._range.end = this._range.start + text.length

    if (options) {
      if (options.start) {
        this._range.end -= options.start
      }
      if (options.end) {
        this._range.end -= options.end
      }
    }

    this._range.length = this._range.end - this._range.start

    this.refocus()
  }

  refocus() {
    window.setTimeout(() => {
      const scroll = this.input.scrollTop
      this.input.focus()
      this.input.scrollTop = scroll

      const caret = this._range.start
      this.input.setSelectionRange(caret, caret + this._range.length)
    }, 250)
  }

  _getRange() {
    if (document.selection) {
      this.input.focus()
      const range = document.selection.createRange()
      const length = range.text.length
      range.moveStart("character", -this.input.value.length)
      return this._createRange(
        this.input,
        range.text.length - length,
        range.text.length
      )
    }

    if (this.input.selectionStart || this.input.selectionStart == "0") {
      return this._createRange(
        this.input,
        this.input.selectionStart,
        this.input.selectionEnd
      )
    }
  }

  _createRange(textarea, start, end) {
    return {
      start: start,
      end: end,
      length: end - start,
      text: textarea.value.substring(start, end),
      prefix: textarea.value.substring(0, start),
      suffix: textarea.value.substring(end),
    }
  }
}

const editor = new MarkupEditor()

export default editor

editor.setAction("strong", function ({ selection }) {
  if (selection.empty()) {
    selection.replace("**" + pgettext("example markup", "Strong text") + "**", {
      start: 2,
      end: 2,
    })
  } else {
    selection.wrap("**", "**")
  }
})

editor.setAction("emphasis", function ({ selection }) {
  if (selection.empty()) {
    selection.replace(
      "_" + pgettext("example markup", "Text with emphasis") + "_",
      { start: 1, end: 1 }
    )
  } else {
    selection.wrap("_", "_")
  }
})

editor.setAction("strikethrough", function ({ selection }) {
  if (selection.empty()) {
    selection.replace(
      "~~" + pgettext("example markup", "Text with strikethrough") + "~~",
      { start: 2, end: 2 }
    )
  } else {
    selection.wrap("~~", "~~")
  }
})

editor.setAction("horizontal-ruler", function ({ selection }) {
  selection.replace("\n\n- - -\n\n", { start: 9 })
})

editor.setAction("link", function ({ editor, selection }) {
  editor.showLinkModal(selection)
})

editor.setAction("image", function ({ editor, selection }) {
  editor.showImageModal(selection)
})

editor.setAction("quote", function ({ editor, selection }) {
  editor.showQuoteModal(selection)
})

editor.setAction("spoiler", function ({ selection }) {
  const prefix = selection.prefix().trim().length
    ? "\n\n[spoiler]\n"
    : "[spoiler]\n"
  const suffix = "\n[/spoiler]\n\n"

  if (selection.empty()) {
    selection.replace(
      prefix + pgettext("example markup", "Spoiler text") + suffix,
      { start: prefix.length, end: suffix.length }
    )
  } else {
    selection.wrap(prefix, suffix)
  }
})

editor.setAction("code", function ({ editor, selection }) {
  editor.showCodeModal(selection)
})

editor.setAction("formatting-help", function ({ target }) {
  const modal = document.getElementById("markup-editor-formatting-help")
  const element = target.closest("a")

  htmx
    .ajax("GET", element.href, {
      target: modal,
      swap: "innerHTML",
    })
    .then(() => {
      $(modal).modal("show")
    })
})
