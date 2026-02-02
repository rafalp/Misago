import { computePosition, flip, offset, shift } from "@floating-ui/dom"
import * as snackbar from "../snackbars"
import QuoteCursorPosition from "./QuoteCursorPosition"
import QuoteSelection from "./QuoteSelection"
import Ruleset from "./Ruleset"
import extractorRules from "./extractor"
import postprocessRules from "./postprocess"
import rendererRules from "./renderer"
import tetherRules from "./tether"

class Quote {
  constructor() {
    this.extractor = new Ruleset(extractorRules)
    this.postprocess = new Ruleset(postprocessRules)
    this.renderer = new Ruleset(rendererRules)
    this.tether = new Ruleset(tetherRules)

    this.selecting = false
    this.debounce = null

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
      document.addEventListener("mousedown", this.onSelectStart)
      document.addEventListener("mouseup", this.onSelectEnd)
      document.addEventListener("selectionchange", this.onSelectChange)

      this.options = options
      this.toolbar = this.createToolbar()
      this.cursor = new QuoteCursorPosition(this.tether)
    }
  }

  onSelectStart = () => {
    this.selecting = true
  }

  onSelectEnd = () => {
    this.selecting = false
    this.updateSelection()
  }

  onSelectChange = () => {
    if (this.selecting) {
      return
    }

    if (this.debounce) {
      window.clearTimeout(this.debounce)
    }

    this.debounce = window.setTimeout(this.updateSelection, 300)
  }

  updateSelection = () => {
    if (this.selecting) {
      return
    }

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
      selection.isCollapsed ||
      selection.type !== "Range" ||
      selection.rangeCount === 0
    ) {
      return false
    }

    const range = this.getRange(selection)
    const root = this.getRangeRoot(range)

    if (!root) {
      return false
    }

    this.range = range
    this.root = root
    this.quote = this.getSelectionQuote(root)

    return this.range && this.root && this.quote
  }

  clearState() {
    this.selecting = true

    this.range = null
    this.root = null
    this.quote = null

    this.hideToolbar()

    window.setTimeout(() => {
      this.selecting = false
    }, 300)
  }

  getRange(selection) {
    if (selection.rangeCount === 1) {
      return selection.getRangeAt(0)
    }

    // Separate logic for FireFox
    // https://bugzilla.mozilla.org/show_bug.cgi?id=753718
    const start = selection.getRangeAt(0)
    const end = selection.getRangeAt(selection.rangeCount - 1)

    const range = new Range()
    range.setStart(start.startContainer, start.startOffset)
    range.setEnd(end.endContainer, end.endOffset)

    return range
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

  getSelectionQuote(root) {
    const selection = new QuoteSelection(
      this.extractor,
      this.renderer,
      this.postprocess
    )

    const quote = selection.getQuote(root)

    if (quote) {
      return "\n\n" + quote + "\n\n"
    }

    return ""
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
    const position = this.cursor.getPosition(this.root, this.range)
    if (!position) {
      return
    }

    this.toolbar.classList.add("show")

    computePosition(position, this.toolbar, {
      placement: "bottom",
      middleware: [offset(4), flip(), shift({ padding: 8 })],
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
    this.updateForm(form, this.quote)
    this.clearState()
  }

  updateForm = (form, quote) => {
    if (form && quote) {
      const input = form.querySelector(".markup-editor-textarea")
      if (input) {
        if (input.value.trim()) {
          input.value += quote
        } else {
          input.value = quote.trimStart()
        }
        snackbar.info(pgettext("quote toolbar", "Quote added to reply"))
      }
    }
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

    this.clearState()
  }
}

const quote = new Quote()

export default quote
