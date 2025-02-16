class MarkupEditorModal {
  constructor() {
    this.selection = null
    this.element = null
    this.form = null

    document.addEventListener("DOMContentLoaded", () => {
      this.element = this.getElement()
      if (this.element) {
        this.form = this.element.querySelector("form")
        this.initForm(this.form)
      }
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

export class MarkupEditorLinkModal extends MarkupEditorModal {
  getElement() {
    return document.getElementById("markup-editor-link-modal")
  }

  setData(form, selection) {
    form.querySelector('[name="text"]').value = selection.text().trim()
  }

  submit(data, selection) {
    const url = cleanUrl(data.get("url").trim())
    const text = data.get("text").trim()

    if (url) {
      if (text) {
        if (isUnsafeForMarkdown(url, text)) {
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

export class MarkupEditorImageModal extends MarkupEditorModal {
  getElement() {
    return document.getElementById("markup-editor-image-modal")
  }

  submit(data, selection) {
    const url = cleanUrl(data.get("url").trim())
    const text = data.get("text").trim()

    if (url) {
      if (text) {
        if (isUnsafeForMarkdown(url, text)) {
          selection.replace("[img=" + url + "]" + text + "[/img]")
        } else {
          selection.replace("![" + text + "](" + url + ")")
        }
      } else if (isUnsafeForMarkdown(url, text)) {
        selection.replace("[img]" + url + "[/img]")
      } else {
        selection.replace("!(" + url + ")")
      }

      this.hide()
    }
  }
}

function isUnsafeForMarkdown(url, text) {
  if (url.indexOf("(") >= 0) return true
  if (url.indexOf(")") >= 0) return true
  if (text.indexOf("[") >= 0) return true
  if (text.indexOf("]") >= 0) return true

  return false
}

function cleanUrl(url) {
  if (startsWith(url, "http://") || startsWith(url, "https://")) {
    return url
  }

  return "http://" + url
}

function startsWith(text, prefix) {
  return text.toLowerCase().substring(0, prefix.length) === prefix
}

export class MarkupEditorQuoteModal extends MarkupEditorModal {
  getElement() {
    return document.getElementById("markup-editor-quote-modal")
  }

  setData(form, selection) {
    form.querySelector('[name="text"]').value = selection.text().trim()
  }

  submit(data, selection) {
    const author = data.get("author").trim()
    const text = data.get("text").trim()

    if (text) {
      const prefix = this.getQuotePrefix(selection, author)
      const suffix = "\n[/quote]\n\n"

      selection.replace(prefix + text + suffix, {
        start: prefix.length,
        end: suffix.length,
      })

      this.hide()
    }
  }

  getQuotePrefix(selection, author) {
    const prefix = selection.prefix().trim().length ? "\n\n" : ""
    if (author) {
      return prefix + "[quote=" + author + "]\n"
    }
    return prefix + "[quote]\n"
  }
}

export class MarkupEditorCodeModal extends MarkupEditorModal {
  getElement() {
    return document.getElementById("markup-editor-code-modal")
  }

  setData(form, selection) {
    form.querySelector('[name="code"]').value = selection.text().trim()
  }

  submit(data, selection) {
    const syntax = data.get("syntax").trim()
    const code = data.get("code").trim()

    if (code) {
      const prefix = this.getQuotePrefix(selection, syntax)
      const suffix = "\n[/code]\n\n"

      selection.replace(prefix + code + suffix, {
        start: prefix.length,
        end: suffix.length,
      })

      this.hide()
    }
  }

  getQuotePrefix(selection, syntax) {
    const prefix = selection.prefix().trim().length ? "\n\n" : ""
    if (syntax) {
      return prefix + "[code=" + syntax + "]\n"
    }
    return prefix + "[code]\n"
  }
}
