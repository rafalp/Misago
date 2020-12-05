export interface IReplaceOptions {
  textarea: HTMLTextAreaElement
  replace?: string
  default?: string
  prefix?: string
  suffix?: string
  trim?: boolean
  lstrip?: RegExp
  rstrip?: RegExp
}

type Mutation<T = string> = (state: State, value: T) => State

type State = {
  selection: Selection
  value: string
}

type Selection = {
  start: number
  end: number
  length: number
  text: string
}

const replaceSelection = (options: IReplaceOptions): State => {
  let state: State = {
    selection: getSelection(options.textarea),
    value: options.textarea.value,
  }

  if (options.default) {
    state = setDefault(state, options.default)
  }

  if (options.trim) {
    state = trim(state, options.trim)
  }

  if (options.lstrip) {
    state = lstrip(state, options.lstrip)
  }

  if (options.rstrip) {
    state = rstrip(state, options.rstrip)
  }

  if (options.replace) {
    state = replace(state, options.replace)
  }

  if (options.prefix) {
    state = prefix(state, options.prefix)
  }

  if (options.suffix) {
    state = suffix(state, options.suffix)
  }

  return state
}

export default replaceSelection

export const getSelection = (textarea: HTMLTextAreaElement): Selection => {
  return {
    start: textarea.selectionStart,
    end: textarea.selectionEnd,
    length: textarea.selectionEnd - textarea.selectionStart,
    text: textarea.value.substring(
      textarea.selectionStart,
      textarea.selectionEnd
    ),
  }
}

export const trim: Mutation<boolean> = (
  { selection, value },
  arg: boolean
): State => {
  if (!arg) return { selection, value }

  const prefix = selection.text.match(/^\s+/)?.[0] || ""
  const suffix = selection.text.match(/\s+$/)?.[0] || ""

  const { start, end, length, text } = selection

  const newSelection = {
    start: start + prefix.length,
    end: end - suffix.length,
    length: length - prefix.length - suffix.length,
    text: text.substring(0, length - suffix.length).substr(prefix.length),
  }

  return { selection: newSelection, value }
}

export const lstrip: Mutation<RegExp> = (
  { selection, value },
  arg: RegExp
): State => {
  const { start, end, length, text } = selection

  const newLeading = value.substr(0, start).replace(arg, "")

  const newSelection = {
    start: newLeading.length,
    end: end - (start - newLeading.length),
    length: length,
    text: text,
  }

  return {
    selection: newSelection,
    value: newLeading + value.substr(start),
  }
}

export const rstrip: Mutation<RegExp> = (
  { selection, value },
  arg: RegExp
): State => {
  const newTrailing = value.substr(selection.end).replace(arg, "")

  return {
    selection,
    value: value.substr(0, selection.end) + newTrailing,
  }
}

export const setDefault: Mutation = (
  { selection, value },
  arg: string
): State => {
  if (selection.length) return { selection, value }

  const newSelection = {
    start: selection.start,
    end: selection.start + arg.length,
    length: arg.length,
    text: arg,
  }

  const { start, end } = selection
  const newValue = value.substr(0, start) + arg + value.substr(end)

  return { selection: newSelection, value: newValue }
}

export const replace: Mutation = (
  { selection, value },
  arg: string
): State => {
  const newSelection = {
    start: selection.start,
    end: selection.start + arg.length,
    length: arg.length,
    text: arg,
  }

  const { start, end } = selection
  const newValue = value.substr(0, start) + arg + value.substr(end)

  return { selection: newSelection, value: newValue }
}

export const prefix: Mutation = ({ selection, value }, arg: string): State => {
  const { start, end, length, text } = selection
  const newSelection = {
    start: start + arg.length,
    end: end + arg.length,
    length: length,
    text: text,
  }

  return {
    selection: newSelection,
    value: value.substr(0, start) + arg + value.substr(end - length),
  }
}

export const suffix: Mutation = ({ selection, value }, arg: string): State => {
  const { start, end, length } = selection
  return {
    selection,
    value: value.substr(0, start + length) + arg + value.substr(end),
  }
}
