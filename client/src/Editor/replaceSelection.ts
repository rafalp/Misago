export interface IReplaceOptions {
  textarea: HTMLTextAreaElement
  replace?: string
  prefix?: string
  suffix?: string
}

type Mutation = (state: State, value: string) => State

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

  console.log("init", state)
  if (options.replace) {
    state = replace(state, options.replace)
  }

  if (options.prefix) {
    state = prefix(state, options.prefix)
    console.log("prefix", state)
  }

  if (options.suffix) {
    state = suffix(state, options.suffix)
    console.log("suffix", state)
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
    length: selection.length,
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
