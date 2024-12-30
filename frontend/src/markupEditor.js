class MarkupEditor {
  constructor() {
    this.actions = {}
    this.linkModal = new MarkupEditorLinkModal()
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
      control.addEventListener("click", ({ target }) => {
        const action = this.actions[actionName]
        if (action) {
          action({
            input,
            target,
            editor: this,
            selection: new MarkupEditorSelection(input),
          })
        } else {
          console.warn("Undefined markup editor action: " + actionName)
        }
      })
    })
  }

  showLinkModal(selection) {
    this.linkModal.show(selection)
  }
}

class MarkupEditorModal {
  constructor() {
    this.selection = null
    this.element = null
    this.form = null

    document.addEventListener("DOMContentLoaded", () => {
      this.element = this.getElement()
      this.form = this.element.querySelector("form")
      this.initForm(this.form)
    })
  }

  getElement() {
    throw "Subclasses of 'MarkupEditorModal' must implement 'getElement' method"
  }

  initForm(form) {
    form.addEventListener("submit", (event) => {
      event.preventDefault()
      const data = new FormData(event.target)
      this.submit(data, this.selection)
      return false
    })
  }

  reset() {
    this.element.querySelectorAll("input").forEach((input) => {
      input.value = ""
    })
  }

  setData(form, selection) {}

  submit(data, selection) {}

  show(selection) {
    this.reset()
    this.selection = selection
    this.setData(this.form, selection)
    $(this.element).modal("show")
  }

  hide() {
    $(this.element).modal("hide")
  }
}

class MarkupEditorLinkModal extends MarkupEditorModal {
  getElement() {
    return document.getElementById("markup-editor-link-modal")
  }

  setData(form, selection) {
    form.querySelector('[name="text"]').value = selection.text().trim()
  }

  submit(data, selection) {
    const url = data.get("url").trim()
    const text = data.get("text").trim()

    if (url) {
      if (text) {
        if (isUrlUnsafeMarkdown(url) || isUrlTextUnsafeMarkdown(text)) {
          selection.replace("[url=" + url + "]" + text + "[/url]")
        } else {
          selection.replace("[" + text + "](" + url + ")")
        }
      } else {
        selection.replace("<" + url + ">")
      }

      this.hide()
    }
  }
}

function isUrlUnsafeMarkdown(value) {
  if (value.indexOf("(") >= 0) return true
  if (value.indexOf(")") >= 0) return true

  return false
}

function isUrlTextUnsafeMarkdown(value) {
  if (value.indexOf("[") >= 0) return true
  if (value.indexOf("]") >= 0) return true

  return false
}

class MarkupEditorSelection {
  constructor(input) {
    this.input = input
    this._range = this._getRange()
  }

  get() {
    return this._range
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

export function activateEditors() {
  document
    .querySelectorAll("[misago-editor-active='false']")
    .forEach(editor.activate)
}
