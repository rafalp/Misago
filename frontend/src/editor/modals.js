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
