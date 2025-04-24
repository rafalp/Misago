export function escapeBBCodeArg(arg) {
  return escapeQuotes(escapeBrackets(escapeBackslash(arg)))
}

export function escapeBBCodeContents(arg) {
  return escapeBrackets(escapeBackslash(arg))
}

export function escapeMarkdownLink(arg) {
  return escapeQuotes(escapeParentheses(escapeBackslash(arg)))
}

export function escapeMarkdownLinkText(arg) {
  return escapeQuotes(escapeBrackets(escapeBackslash(arg)))
}

export function escapeMarkdownLinkTitle(arg) {
  return escapeMarkdownLink(arg)
}

export function escapeMarkdownImageTitle(arg) {
  let escaped = escapeBackslash(arg)
  escaped = escaped.replace("(", "\\(")
  escaped = escaped.replace(")", "\\)")
  return escaped.replace('"', '\\"')
}

export function escapeAutolink(arg) {
  return escapeBackslash(arg).replaceAll("<", "\\<").replaceAll(">", "\\>")
}

export function escapeInlineCode(arg) {
  return escapeBackslash(arg).replaceAll("`", "\\`").replaceAll("`", "\\`")
}

export function escapeBackslash(text) {
  return text.replaceAll("\\", "\\\\")
}

export function escapeBrackets(text) {
  return text.replaceAll("[", "\\[").replaceAll("]", "\\]")
}

export function escapeParentheses(text) {
  return text.replaceAll("(", "\\(").replaceAll(")", "\\)")
}

export function escapeQuotes(text) {
  return text.replace('"', '\\"').replace("'", "\\'")
}
