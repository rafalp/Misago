import { computePosition, flip, offset, shift } from "@floating-ui/dom"
import * as snackbar from "../snackbars"

class Quote {
  constructor() {
    this.options = null
    this.toolbar = null

    this.range = null
    this.root = null
  }

  activate = (options) => {
    if (
      (options.reply || options.quote) &&
      typeof window.getSelection !== "undefined"
    ) {
      document.addEventListener("mouseup", this.onSelect)
      document.addEventListener("touchend", this.onSelect)

      this.options = options
      this.toolbar = this.createToolbar()
    }
  }

  onSelect = () => {
    if (this.updateState()) {
      this.showToolbar()
    } else {
      this.hideToolbar()
    }
  }

  updateState() {
    this.range = null
    this.root = null

    const selection = window.getSelection()
    if (
      !selection ||
      selection.type !== "Range" ||
      selection.rangeCount !== 1
    ) {
      return false
    }

    const range = selection.getRangeAt(0)
    const root = this.getRangeRoot(range)

    if (!root) {
      return false
    }

    this.range = range
    this.root = root

    return this.range && this.root
  }

  getRangeRoot(range) {
    const ancestor = this.getCommonAncestor(range)
    if (!ancestor) {
      return null
    }

    const root = ancestor.closest("[misago-quote-root]")
    if (root) {
      return {
        element: root,
        args: root.getAttribute("misago-quote-root"),
      }
    }
    return null
  }

  getCommonAncestor(range) {
    const ancestor = range.commonAncestorContainer
    if (!ancestor) {
      return null
    } else if (ancestor.nodeType === Node.TEXT_NODE) {
      return ancestor.parentNode
    }
    return ancestor
  }

  createToolbar() {
    const toolbar = document.createElement("div")
    toolbar.className = "quote-toolbar"

    if (this.options.reply) {
      const reply = this.createToolbarButton(
        pgettext("quote toolbar", "Reply"),
        "reply",
        this.reply
      )
      toolbar.appendChild(reply)
    }

    if (this.options.quote) {
      const quote = this.createToolbarButton(
        pgettext("quote toolbar", "Copy quote"),
        "content_copy",
        this.copyQuote
      )
      toolbar.appendChild(quote)
    }

    document.body.appendChild(toolbar)

    return toolbar
  }

  createToolbarButton(text, icon, callback) {
    const btn = document.createElement("button")
    btn.className = "quote-toolbar-btn"

    const btnIcon = document.createElement("span")
    btnIcon.className = "material-icon"
    btnIcon.innerText = icon
    btn.appendChild(btnIcon)

    const btnText = document.createElement("span")
    btnText.className = "quote-toolbar-btn-text"
    btnText.innerText = text
    btn.appendChild(btnText)

    btn.addEventListener("click", callback)
    return btn
  }

  showToolbar() {
    this.toolbar.classList.add("show")

    computePosition(this.range, this.toolbar, {
      placement: "top",
      middleware: [offset(6), flip(), shift({ padding: 8 })],
    }).then(({ x, y }) => {
      Object.assign(this.toolbar.style, {
        left: `${x}px`,
        top: `${y}px`,
      })
    })
  }

  hideToolbar() {
    this.toolbar.classList.remove("show")
  }

  reply = () => {
    const form = document.getElementById("misago-htmx-quick-reply")
    const text = this.getQuoteText()

    if (form && text) {
      const textarea = form.querySelector(".markup-editor-textarea")
      if (textarea) {
        textarea.value += text
        snackbar.info(pgettext("quote toolbar", "Quote added to reply"))
      }
    }

    this.hideToolbar()
  }

  copyQuote = async () => {
    const text = this.getQuoteText()

    if (text) {
      try {
        await navigator.clipboard.writeText(text)
        snackbar.info(pgettext("quote toolbar", "Quote copied to clipboard"))
      } catch (error) {
        console.error(error.message)
      }
    }

    this.hideToolbar()
  }

  getQuoteText() {
    const markup = this.getSelectionMarkup()
    if (!markup) {
      return ""
    }

    let text = "\n[quote=" + this.root.args + "]"
    text += "\n" + markup
    text += "\n[/quote]\n"

    return text
  }

  getSelectionMarkup() {
    const nodes = this.range.cloneContents().childNodes

    let markup = ""
    for (let i = 0; i < nodes.length; i++) {
      const node = nodes[i]
      if (node.nodeType === Node.TEXT_NODE) {
        markup += node.textContent || ""
      } else if (node.nodeName === "A") {
        markup +=
          "[url=" +
          node.getAttribute("href") +
          "]" +
          node.textContent +
          "[/url]"
      }
    }
    return markup
  }
}

const quote = new Quote()

export default quote
