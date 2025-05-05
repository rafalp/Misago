export default function getQuotedCode(node) {
  const code = getCodeTextContent(node)
  return dedentTrimCode(code)
}

function getCodeTextContent(node) {
  let text = ""
  for (let i = 0; i < node.childNodes.length; i++) {
    const child = node.childNodes[i]
    if (child.nodeType === Node.TEXT_NODE) {
      text += child.textContent
    } else if (child.nodeName === "SPAN") {
      text += getCodeTextContent(child)
    }
  }
  return text
}

function dedentTrimCode(code) {
  const lines = splitLines(trimCodeBlankLines(code))

  let dedent = -1
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    if (line.trim()) {
      const lineDedent = lines[i].length - lines[i].trimStart().length
      if (dedent === -1 || lineDedent < dedent) {
        dedent = lineDedent
      }
    }
  }

  if (dedent) {
    for (let i = 0; i < lines.length; i++) {
      lines[i] = lines[i].substring(dedent)
    }
  }

  return lines.join("\n")
}

function trimCodeBlankLines(code) {
  const cleanLines = []
  const lines = splitLines(code)
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    if (cleanLines.length || line.trim()) {
      cleanLines.push(line.trimEnd())
    }
  }
  return cleanLines.join("\n").trimEnd()
}

function splitLines(text) {
  return text.split(/\r?\n/)
}
