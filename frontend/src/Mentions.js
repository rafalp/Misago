import { createAutocomplete } from "@algolia/autocomplete-core"

const BEFORE_RE = /[^\w]@[a-z0-9_-]*$/gi
const AFTER_RE = /^[a-z0-9_-]*/gi
const FULL_RE = /[^\w]@[a-z0-9_-]+$/gi

class Mentions {
  constructor() {
    this.autocomplete = null
  }

  getMentions() {
    if (!this.autocomplete) {
      this.autocomplete = this.createAutocomplete()
    }

    return this.autocomplete
  }

  createAutocomplete() {
    return createAutocomplete({
      getSources() {
        return [
          {
            sourceId: "misagoUserMention",
            getItemInputValue: ({ item }) => item.query,
            getItems({ query }) {
              console.log(query)
              return []
            },
          },
        ]
      },
    })
  }

  activate = (control) => {
    control.addEventListener("mouseup", this.onInput)
    control.addEventListener("keyup", this.onInput)
  }

  onInput = (event) => {
    const selection = this.getSelection(event.target)
    const mention = this.getSelectionMention(selection)
    console.log(selection, mention)
  }

  getSelectionMention(selection) {
    const { start, end, closed, before, after, value } = selection

    const behindMatch = before.match(BEFORE_RE)
    const aheadMatch = after.match(AFTER_RE)
    const fullMatch = (before + value).match(FULL_RE)

    const prefix = behindMatch ? behindMatch[0].trim() : ""
    const suffix = aheadMatch ? aheadMatch[0].trim() : ""
    const full = fullMatch ? fullMatch[0].trim() : ""

    if (closed) {
      if (prefix && suffix) {
        const mention = prefix + suffix
        return {
          start: start - prefix.length,
          end: end + suffix.length,
          mention,
        }
      } else if (prefix) {
        const mention = prefix
        return {
          start: start - prefix.length,
          end: end,
          mention,
        }
      }

      return null
    } else if (prefix && suffix) {
      return {
        start: start - prefix.length,
        end: end + suffix.length,
        mention: prefix + value + suffix,
      }
    } else if (prefix) {
      return {
        start: start - prefix.length,
        end: end,
        mention: prefix + value,
      }
    } else if (full && suffix) {
      return {
        start: start - prefix.length,
        end: end + suffix.length,
        mention: full + suffix,
      }
    } else if (full) {
      return {
        start: start,
        end: end,
        mention: full,
      }
    }

    return null
  }

  getSelection(control) {
    const text = control.value
    const selectionStart = control.selectionStart
    const selectionEnd = control.selectionEnd

    const before = text.substring(0, selectionStart)
    const after = text.substring(selectionEnd)
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
      after,
    }
  }
}

export default Mentions

const mentions = new Mentions()

export { mentions }
