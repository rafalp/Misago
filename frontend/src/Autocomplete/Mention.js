import select from "./Select"
import suggestions from "./Suggestions"

const BEFORE_RE = /(^|[^\p{L}\p{N}])@[a-z0-9_\-]*$/giu
const AHEAD_RE = /^[\p{L}\p{N}]/giu

const INVALID_KEYS = {
  Delete: true,
  Space: true,
  MetaLeft: true,
  End: true,
  ArrowLeft: true,
  ArrowUp: true,
  ArrowRight: true,
  ArrowDown: true,
}

const DEBOUNCE = 800

class Mention {
  constructor(control) {
    this.control = control
    this.debounce = null

    control.addEventListener("keyup", this.onKeyUp)
  }

  onKeyUp = (event) => {
    if (INVALID_KEYS[event.code]) {
      select.hide()
      return false
    }

    const selection = this.getSelection(event.target)
    const query = this.getSelectionQuery(selection)

    if (query) {
      this.getSuggestions(query)
    } else {
      select.hide()
    }
  }

  getSelection(control) {
    const text = control.value
    const selectionStart = control.selectionStart
    const selectionEnd = control.selectionEnd

    const before = text.substring(0, selectionStart)
    const ahead = text.substring(selectionEnd)
    const value =
      selectionStart < selectionEnd
        ? text.substring(selectionStart, selectionEnd)
        : ""

    return {
      text,
      start: selectionStart,
      end: selectionEnd,
      closed: selectionStart === selectionEnd,
      value,
      before,
      ahead,
    }
  }

  getSelectionQuery(selection) {
    const { start, end, closed, before, ahead } = selection

    if (!closed) {
      return null
    }

    const beforeMatch = before.match(BEFORE_RE)
    const aheadMatch = ahead.match(AHEAD_RE)

    const prefix = beforeMatch ? beforeMatch[0].trim() : ""
    const suffix = aheadMatch ? aheadMatch[0].trim() : ""

    if (prefix.length < 3 || suffix) {
      return null
    }

    return {
      start: start - prefix.length,
      end: end,
      text: prefix.substring(1),
    }
  }

  getSuggestions(query) {
    if (!!this.debounce) {
      window.clearTimeout(this.debounce)
    }

    this.debounce = window.setTimeout(() => {
      suggestions.get(query.text).then((results) => {
        select.show(this.control, query, results)
      })
    }, DEBOUNCE)
  }
}

export default Mention
