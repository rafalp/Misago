import { computePosition, flip, offset, shift } from "@floating-ui/dom"
import * as snackbar from "../snackbars"
import QuoteCursorPosition from "./QuoteCursorPosition"
import QuoteSelection from "./QuoteSelection"
import Ruleset from "./Ruleset"
import extractorRules from "./extractor"
import postprocessRules from "./postprocess"
import rendererRules from "./renderer"

class Quote {
  constructor() {
    this.extractor = new Ruleset(extractorRules)
    this.postprocess = new Ruleset(postprocessRules)
    this.renderer = new Ruleset(rendererRules)

    this.options = null
    this.toolbar = null
    this.cursor = null

    this.range = null
    this.root = null
    this.quote = null
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
      this.cursor = new QuoteCursorPosition()
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
    this.quote = null

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
    this.quote = this.getSelectionQuote(root, range) || null

    return this.range && this.root && this.quote
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
        info: root.getAttribute("misago-quote-root"),
        ancestor,
        childNodes: range.cloneContents().childNodes,
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

  getSelectionQuote(root, range) {
    const selection = new QuoteSelection(
      this.extractor,
      this.renderer,
      this.postprocess
    )
    return "\n\n" + selection.getQuote(root) + "\n\n"
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
    const position = this.cursor.getPosition(this.root.element, this.range)

    this.toolbar.classList.add("show")

    computePosition(position, this.toolbar, {
      placement: "bottom",
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

    if (form && this.quote) {
      const textarea = form.querySelector(".markup-editor-textarea")
      if (textarea) {
        if (textarea.value.trim()) {
          textarea.value += this.quote
        } else {
          textarea.value = this.quote.trimStart()
        }
        snackbar.info(pgettext("quote toolbar", "Quote added to reply"))
      }
    }

    this.hideToolbar()
  }

  copyQuote = async () => {
    if (this.quote) {
      try {
        await navigator.clipboard.writeText(this.quote)
        snackbar.info(pgettext("quote toolbar", "Quote copied to clipboard"))
      } catch (error) {
        console.error(error.message)
      }
    }

    this.hideToolbar()
  }
}

const quote = new Quote()

export default quote
