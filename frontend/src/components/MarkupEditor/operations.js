const wrapSelection = (selection, update, prefix, suffix, def) => {
  const text = selection.text || def || ""
  let newValue = selection.prefix
  newValue += prefix + text + suffix
  newValue += selection.suffix
  update(newValue)

  window.setTimeout(() => {
    focus(selection.textarea)

    const caret = selection.start + prefix.length
    selection.textarea.setSelectionRange(caret, caret + text.length)
  }, 250)
}

const replaceSelection = (selection, update, text) => {
  let newValue = selection.prefix
  newValue += text
  newValue += selection.suffix
  update(newValue)

  window.setTimeout(() => {
    focus(selection.textarea)

    const caret = selection.end + text.length
    selection.textarea.setSelectionRange(caret, caret)
  }, 250)
}

const getSelection = (textarea) => {
  if (document.selection) {
    textarea.focus()
    const range = document.selection.createRange()
    const length = range.text.length
    range.moveStart("character", -textarea.value.length)
    return createRange(textarea, range.text.length - length, range.text.length)
  }

  if (textarea.selectionStart || textarea.selectionStart == "0") {
    return createRange(textarea, textarea.selectionStart, textarea.selectionEnd)
  }
}

const createRange = (textarea, start, end) => {
  return {
    textarea: textarea,
    start: start,
    end: end,
    text: textarea.value.substring(start, end),
    prefix: textarea.value.substring(0, start),
    suffix: textarea.value.substring(end),
  }
}

export function focus(textarea) {
  const scroll = textarea.scrollTop
  textarea.focus()
  textarea.scrollTop = scroll
}

export { getSelection, replaceSelection, wrapSelection }
