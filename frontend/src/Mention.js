import { Autocomplete, AnchorInput, SelectUser, sources } from "./Autocomplete"

const RE_LOOKBACK = /(^|[^\p{L}\p{N}])@[a-z0-9_\-]*$/giu
const RE_LOOKAHEAD = /^[\p{L}\p{N}]/giu

class Mention {
  constructor(control) {
    this.autocomplete = new Autocomplete({
      control,
      source: sources.users,
      select: new SelectUser({
        anchor: new AnchorInput(control),
        placement: "top",
      }),
      getQuery: this.getQuery,
      onSelect: this.onSelect,
    })
  }

  getQuery = (control) => {
    const { start, end, closed, prefix, suffix } = this.getSelection(control)

    if (!closed) {
      return null
    }

    const prefixMatch = prefix.match(RE_LOOKBACK)
    const suffixMatch = suffix.match(RE_LOOKAHEAD)

    const prefixMatchClean = prefixMatch ? prefixMatch[0].trim() : ""
    const suffixMatchClean = suffixMatch ? suffixMatch[0].trim() : ""

    if (prefixMatchClean.length < 2 || suffixMatchClean) {
      return null
    }

    return {
      control,
      start: start - prefixMatchClean.length,
      end: end,
      prefix: prefix.substring(0, start - prefixMatchClean.length + 1),
      value: prefixMatchClean.substring(1),
    }
  }

  getSelection(control) {
    const text = control.value
    const selectionStart = control.selectionStart
    const selectionEnd = control.selectionEnd

    const prefix = text.substring(0, selectionStart)
    const suffix = text.substring(selectionEnd)
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
      prefix,
      suffix,
    }
  }

  onSelect = (choice, query) => {
    const { control, start, end } = query
    const { username } = choice

    const value = control.value
    const prefix = value.substring(0, start)
    const suffix = value.substring(end)
    control.value = prefix + "@" + username + " " + suffix

    window.setTimeout(() => {
      const scroll = control.scrollTop
      control.focus()
      control.scrollTop = scroll

      const caret = start + username.length + 2
      control.setSelectionRange(caret, caret)
    }, 100)
  }
}

export default Mention
