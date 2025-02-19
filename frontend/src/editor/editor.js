import htmx from "htmx.org"
import * as animations from "../animations"
import MarkupEditorUploader from "./uploader"
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

    this.resizeDebounce = null

    window.addEventListener("resize", (event) => {
      if (this.resizeDebounce) {
        window.clearTimeout(this.resizeDebounce)
      }

      this.resizeDebounce = window.setTimeout(this._onWindowResize, 200)
    })
  }

  _onWindowResize = () => {
    document
      .querySelectorAll("[misago-editor-active]")
      .forEach(this._resizeEditor)
  }

  _resizeEditor = (element) => {
    const constraints = this._getResizeConstraints(element)
    const firstToolbar = element.querySelector(".markup-editor-toolbar-left")
    const secondToolbar = element.querySelector(
      ".markup-editor-toolbar-secondary"
    )
    const moreBtn = element.querySelector("[misago-editor-more]")

    let takenSpace = 0
    const items = []
    for (let i = 0; i < firstToolbar.children.length; i++) {
      const child = firstToolbar.children[i]
      if (child.getAttribute("misago-editor-more") !== "true") {
        items.push({
          index: i,
          priority: parseInt(child.getAttribute("misago-editor-priority") || 0),
          display: true,
        })

        if (child.clientWidth) {
          takenSpace += constraints.btn
        }
      }
    }

    if (takenSpace > constraints.toolbar) {
      const limit = constraints.toolbar - constraints.btn
      items.sort((a, b) => {
        if (a.priority > b.priority) {
          return 1
        } else if (a.priority < b.priority) {
          return -1
        }
        return 0
      })

      items.forEach((item) => {
        if (takenSpace > limit) {
          firstToolbar.children[item.index].classList.add("d-none")
          secondToolbar.children[item.index].classList.remove("d-none")
          item.display = false
          takenSpace -= constraints.btn
        } else {
          firstToolbar.children[item.index].classList.remove("d-none")
          secondToolbar.children[item.index].classList.add("d-none")
          item.display = true
        }
      })
    } else if (takenSpace + constraints.btn < constraints.toolbar) {
      takenSpace = 0
      const limit = constraints.toolbar
      items.sort((a, b) => {
        if (a.priority > b.priority) {
          return -1
        } else if (a.priority < b.priority) {
          return 1
        }
        return 0
      })

      items.forEach((item) => {
        if (takenSpace + constraints.btn < limit) {
          firstToolbar.children[item.index].classList.remove("d-none")
          secondToolbar.children[item.index].classList.add("d-none")
          item.display = true
          takenSpace += constraints.btn
        } else {
          firstToolbar.children[item.index].classList.add("d-none")
          secondToolbar.children[item.index].classList.remove("d-none")
          item.display = false
        }
      })
    }

    if (items.filter((item) => !item.display).length === 0) {
      moreBtn.classList.add("d-none")
      secondToolbar.classList.remove("show")
    } else {
      moreBtn.classList.remove("d-none")
    }
  }

  _getResizeConstraints = (element) => {
    const toolbar = element.querySelector(".markup-editor-toolbar-left")

    let btnWidth = 0
    toolbar.querySelectorAll("button").forEach((child) => {
      let childWidth = child.clientWidth
      const childStyle = window.getComputedStyle(child)
      childWidth += parseInt(parseFloat(childStyle.borderLeftWidth))
      childWidth += parseInt(parseFloat(childStyle.borderRightWidth))
      childWidth += parseInt(parseFloat(childStyle.marginLeft))
      childWidth += parseInt(parseFloat(childStyle.marginRight))

      if (childWidth > btnWidth) {
        btnWidth = childWidth
      }
    })

    const toolbarWidth = toolbar.parentElement.clientWidth - btnWidth

    return {
      btn: btnWidth,
      toolbar: toolbarWidth,
    }
  }

  setAction = (name, init) => {
    this.actions[name] = init
  }

  activate = (element) => {
    if (element.getAttribute("misago-editor-active") !== "true") {
      this._setEditorActive(element)
      this._setEditorFocus(element)
      this._setEditorActions(element)
      this._setEditorPasteUpload(element)
      this._setEditorDropUpload(element)
      this._resizeEditor(element)
    }
  }

  _setEditorActive(element) {
    element.setAttribute("misago-editor-active", "true")
  }

  _setEditorFocus(element) {
    const focusEvents = ["focusin", "click"]
    const className = "markup-editor-focused"

    focusEvents.forEach((event) => {
      element.addEventListener(event, () => {
        element.classList.add(className)
      })
    })

    focusEvents.forEach((event) => {
      document.addEventListener(event, (event) => {
        if (!element.contains(event.target)) {
          element.classList.remove(className)
        }
      })
    })
  }

  _setEditorActions(element) {
    const textarea = this.getTextarea(element)

    element.addEventListener("click", (event) => {
      const target = event.target.closest("[misago-editor-action]")
      if (!target) {
        return null
      }

      const actionName = target.getAttribute("misago-editor-action")
      if (!actionName) {
        return null
      }

      event.preventDefault()

      const action = this.actions[actionName]
      if (action) {
        action({
          textarea,
          target,
          editor: this,
          selection: new MarkupEditorSelection(textarea),
        })
      } else {
        console.warn("Undefined editor action: " + actionName)
      }
    })

    element
      .querySelector("[misago-editor-more]")
      .addEventListener("click", () => {
        const secondToolbar = element.querySelector(
          ".markup-editor-toolbar-secondary"
        )
        if (secondToolbar.classList.contains("show")) {
          secondToolbar.classList.remove("show")
        } else {
          secondToolbar.classList.add("show")
        }
      })
  }

  _setEditorPasteUpload = (element) => {
    element.addEventListener("paste", (event) => {
      if (event.clipboardData.files.length) {
        const uploader = new MarkupEditorUploader(this, element)
        if (!uploader.canUpload) {
          uploader.showPermissionDeniedError()
        } else {
          event.preventDefault()
          const textarea = event.target.closest("textarea")
          uploader.uploadFiles(event.clipboardData.files, textarea)
        }
      }
    })
  }

  _setEditorDropUpload = (element) => {
    const className = "markup-editor-drag-drop"
    const elements = [element.querySelector("textarea")]

    const attachments = element.querySelector("[misago-editor-attachments]")
    if (attachments) {
      elements.push(attachments)
    }

    elements.forEach((child) => {
      child.addEventListener("drop", (event) => {
        const uploader = new MarkupEditorUploader(this, element)
        if (event.dataTransfer.files.length) {
          event.preventDefault()
          if (!uploader.canUpload) {
            uploader.showPermissionDeniedError()
          } else if (event.dataTransfer.files) {
            const textarea = event.target.closest("textarea")
            uploader.uploadFiles(event.dataTransfer.files, textarea)
          }
        }

        child.classList.remove(className)
      })

      child.addEventListener("dragenter", (event) => {
        event.preventDefault()
      })

      child.addEventListener("dragleave", () => {
        child.classList.remove(className)
      })

      child.addEventListener("dragover", (event) => {
        child.classList.add(className)
        event.preventDefault()
      })
    })
  }

  getTextarea(element) {
    return element.querySelector("textarea")
  }

  getSelection(textarea) {
    return new MarkupEditorSelection(textarea)
  }

  showFilePrompt(element, options) {
    const uploader = new MarkupEditorUploader(
      this,
      element.closest("[misago-editor-active]")
    )

    if (!uploader.canUpload) {
      uploader.showPermissionDeniedError()
    } else {
      uploader.prompt(options)
    }
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

  getAttachmentByKey(key) {
    return document.querySelector('[misago-editor-upload-key="' + key + '"]')
  }

  removeAttachmentElement(element) {
    const list = element.closest("ul")

    animations.deleteElement(element, function () {
      if (!list.querySelector("li")) {
        const container = list.closest(".markup-editor-attachments-list")
        container.classList.add("d-none")
      }
    })
  }
}

class MarkupEditorSelection {
  constructor(textarea) {
    this.textarea = textarea
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

    this.textarea.value = value

    this._range.start += prefix.length
    this._range.end += prefix.length
    this._range.length = this._range.end - this._range.start

    this.refocus()
  }

  replace(text, options) {
    const value = this._range.prefix + text + this._range.suffix
    this.textarea.value = value

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

  insert(text, options) {
    const whitespace = (options && options.whitespace) || ""

    const prefix = whitespace
      ? this._range.prefix.trimEnd()
      : this._range.prefix
    const suffix = whitespace ? this._range.suffix.trim() : this._range.suffix

    let whitespaces = 1
    let value = prefix

    if (prefix.length && whitespace) {
      value += whitespace
      whitespaces += 1
    }

    value += text + whitespace + suffix
    this.textarea.value = value

    const caret = prefix.length + text.length + whitespace.length * whitespaces
    this._range.end = this._range.start = caret
    this._range.length = 0

    this.refocus()
  }

  replaceAttachments(callback) {
    this.textarea.value = this.textarea.value.replace(
      /<attachment=(.+?)>/gi,
      function (match, p1) {
        if (p1.match(/:/g).length !== 1) {
          return match
        }

        let value = p1.trim()
        while (value.substring(0, 1) === '"') {
          value = value.substring(1)
        }
        while (value.substring(value.length - 1) === '"') {
          value = value.substring(0, value.length - 1)
        }

        const name = value.substring(0, value.indexOf(":")).trim()
        const id = value.substring(value.indexOf(":") + 1).trim()

        if ((name, id)) {
          const result = callback({ match, name, id })
          if (typeof result === "string" || result instanceof String) {
            return result
          }
        }

        return match
      }
    )
  }

  refocus() {
    window.setTimeout(() => {
      const scroll = this.textarea.scrollTop
      this.textarea.focus()
      this.textarea.scrollTop = scroll

      const caret = this._range.start
      this.textarea.setSelectionRange(caret, caret + this._range.length)
    }, 250)
  }

  _getRange() {
    if (document.selection) {
      this.textarea.focus()
      const range = document.selection.createRange()
      const length = range.text.length
      range.moveStart("character", -this.textarea.value.length)
      return this._createRange(
        this.textarea,
        range.text.length - length,
        range.text.length
      )
    }

    if (this.textarea.selectionStart || this.textarea.selectionStart == "0") {
      return this._createRange(
        this.textarea,
        this.textarea.selectionStart,
        this.textarea.selectionEnd
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
  selection.insert("- - -", { whitespace: "\n\n" })
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

editor.setAction("attachment", function ({ target, selection }) {
  const attachment = target.getAttribute("misago-editor-attachment")
  if (attachment) {
    selection.insert("<attachment=" + attachment + ">", { whitespace: "\n\n" })
  }
})

editor.setAction("image-upload", function ({ editor, target }) {
  editor.showFilePrompt(target, { accept: "image", insert: true })
})

editor.setAction("attachment-upload", function ({ editor, target }) {
  editor.showFilePrompt(target)
})

editor.setAction("attachment-delete", function ({ editor, target, selection }) {
  const attachment = target.getAttribute("misago-editor-attachment")
  const name = target
    .closest("[misago-editor-deleted-attachments-name]")
    .getAttribute("misago-editor-deleted-attachments-name")

  selection.replaceAttachments(function ({ id }) {
    if (id === attachment) {
      return ""
    }

    return false
  })

  const element = target.closest("li")
  editor.removeAttachmentElement(element)

  const input = document.createElement("input")
  input.setAttribute("type", "hidden")
  input.setAttribute("name", name)
  input.setAttribute("value", attachment)

  const attachments = target.closest("[misago-editor-attachments]")
  attachments.appendChild(input)
})

editor.setAction(
  "attachment-error-dismiss",
  function ({ editor, target, selection }) {
    const key = target.getAttribute("misago-editor-attachment-key")

    selection.replaceAttachments(function (attachment) {
      if (attachment.id === key) {
        return ""
      }

      return false
    })

    const message = document.querySelector(
      '[misago-editor-attachment-error="' + key + '"]'
    )
    if (message) {
      animations.deleteElement(message)
    }

    const attachment = editor.getAttachmentByKey(key)
    if (attachment) {
      editor.removeAttachmentElement(attachment)
    }
  }
)

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
