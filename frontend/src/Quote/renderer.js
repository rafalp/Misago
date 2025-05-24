import {
  escapeAutolink,
  escapeBBCodeArg,
  escapeBBCodeContents,
  escapeInlineCode,
  escapeMarkdownLink,
  escapeMarkdownLinkText,
  escapeMarkdownLinkTitle,
  escapeTableCell,
} from "./escape"

function attachment(selection, state) {
  const { node } = state

  if (node.type !== "attachment") {
    return false
  }

  if (state.text) {
    if (state.nodes[state.pos - 1].type === "attachment") {
      state.text += "\n"
    } else {
      state.text += "\n\n"
    }
  }

  state.text += "<attachment=" + node.args + ">"
  state.pos += 1

  return true
}

function youtube(selection, state) {
  const { node } = state

  if (node.type !== "youtube") {
    return false
  }

  if (state.text) {
    state.text += "\n\n"
  }

  state.text += node.url
  state.pos += 1

  return true
}

function header(selection, state) {
  const { node } = state

  if (node.type !== "header") {
    return false
  }

  const text = selection.renderNodes(node.children).trim()
  if (!text) {
    return false
  }

  if (state.text) {
    state.text += "\n\n"
  }

  const prefix = "#".repeat(node.level)
  state.text += prefix + " " + text
  state.pos += 1

  return true
}

function quote(selection, state) {
  const { node } = state

  if (node.type !== "quote") {
    return false
  }

  const text = selection.renderNodes(node.children).trim()
  if (!text) {
    return false
  }

  if (state.text) {
    state.text += "\n\n"
  }

  const { info } = node

  state.text += "[quote" + (info ? "=" + escapeBBCodeArg(info) : "") + "]\n"
  state.text += text
  state.text += "\n[/quote]"
  state.pos += 1

  return true
}

function code(selection, state) {
  const { node } = state

  if (node.type !== "code") {
    return false
  }

  const { info, content } = node

  if (!node.content) {
    return false
  }

  if (state.text) {
    state.text += "\n\n"
  }

  state.text += "[code" + (info ? "=" + escapeBBCodeArg(info) : "") + "]\n"
  state.text += content
  state.text += "\n[/code]"
  state.pos += 1

  return true
}

function spoiler(selection, state) {
  const { node } = state

  if (node.type !== "spoiler") {
    return false
  }

  const text = selection.renderNodes(node.children).trim()
  if (!text) {
    return false
  }

  if (state.text) {
    state.text += "\n\n"
  }

  const { info } = node

  state.text += "[spoiler" + (info ? "=" + escapeBBCodeArg(info) : "") + "]\n"
  state.text += text
  state.text += "\n[/spoiler]"
  state.pos += 1

  return true
}

function paragraph(selection, state) {
  const { node } = state

  if (node.type !== "paragraph") {
    return false
  }

  const text = selection.renderNodes(node.children).trim()
  if (!text) {
    return false
  }

  if (state.text) {
    state.text += "\n\n"
  }

  state.text += text
  state.pos += 1

  return true
}

function table(selection, state) {
  const { node } = state

  if (node.type !== "table") {
    return false
  }

  if (state.text) {
    state.text += "\n\n"
  }

  const alignment = []
  const lengths = []
  const rows = []

  // thead.tr.th
  node.children.forEach(function (tbody) {
    if (tbody.type === "table_head") {
      const row = tbody.children[0].children.map(function (cell) {
        const text = getTableCellText(selection, cell)
        alignment.push(cell.alignment)
        lengths.push(Math.max(text.length, 3))
        return text
      })
      rows.push(row)
    } else if (tbody.type === "table_body") {
      tbody.children.forEach(function (table_row) {
        const row = table_row.children.map(function (cell, index) {
          const text = getTableCellText(selection, cell)
          lengths[index] = Math.max(text.length, lengths[index] || 0, 3)
          return text
        })
        rows.push(row)
      })
    }
  })

  const table = []
  rows.forEach(function (cols, index) {
    const row = cols.map(function (text, col) {
      return text + " ".repeat(lengths[col] - text.length)
    })

    table.push("| " + row.join(" | ") + " | ")

    if (index === 0) {
      const header = cols.map(function (_, col) {
        if (alignment[col] === "l") {
          return "-".repeat(lengths[col])
        } else if (alignment[col] === "r") {
          return "-".repeat(lengths[col] - 1) + ":"
        } else if (alignment[col] === "c") {
          return ":" + "-".repeat(lengths[col] - 2) + ":"
        }
      })
      table.push("| " + header.join(" | ") + " | ")
    }
  })

  state.text += table.join("\n")
  state.pos += 1

  return true
}

function getTableCellText(selection, node) {
  return escapeTableCell(selection.renderNodes(node.children).trim())
}

function list(selection, state) {
  const { node } = state

  if (node.type !== "list") {
    return false
  }

  if (state.text) {
    state.text += "\n\n"
  }

  const items = node.children.map((item, index) => {
    const prefix = node.ordered ? index + 1 + ". " : "* "
    const text = selection.renderNodes(item.children).trim()
    const lines = text.split(/\r?\n|\r|\n/g).map((line, lineIndex) => {
      if (lineIndex === 0) {
        return prefix + line.trim()
      } else {
        return " ".repeat(prefix.length) + line.trim()
      }
    })
    return lines.join("\n")
  })

  state.text += items.join("\n")
  state.pos += 1

  return true
}

function hr(selection, state) {
  const { node } = state

  if (node.type !== "hr") {
    return false
  }

  if (state.text) {
    state.text += "\n\n"
  }

  state.text += "- - -"
  state.pos += 1

  return true
}

function image(selection, state) {
  const { node } = state

  if (node.type !== "image") {
    return false
  }

  const { url, alt, title } = node

  if (alt || title) {
    state.text += "!"
    if (alt) {
      state.text += "[" + escapeMarkdownLinkText(alt) + "]"
    }
    state.text += "(" + escapeMarkdownLink(url)
    if (title) {
      state.text += ' "' + escapeMarkdownLinkTitle(title) + '"'
    }
    state.text += ")"
  } else {
    state.text += "[img]" + escapeBBCodeContents(url) + "[/img]"
  }

  state.pos += 1

  return true
}

function link(selection, state) {
  const { node } = state

  if (node.type !== "link") {
    return false
  }

  const { auto, children, href } = node
  const text = selection.renderNodes(children)

  if (auto) {
    state.text += "<" + escapeAutolink(href) + ">"
  } else {
    state.text += "[url=" + escapeBBCodeArg(href) + "]" + text + "[/url]"
  }

  state.pos += 1

  return true
}

function strong_text(selection, state) {
  const { node } = state

  if (node.type !== "strong") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  const delimiter = text.indexOf("_") === -1 ? "__" : "**"
  state.text += delimiter + text + delimiter
  state.pos += 1

  return true
}

function emphasis_text(selection, state) {
  const { node } = state

  if (node.type !== "emphasis") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  const delimiter = text.indexOf("_") === -1 ? "_" : "**"
  state.text += delimiter + text + delimiter
  state.pos += 1

  return true
}

function bold_text(selection, state) {
  const { node } = state

  if (node.type !== "bold") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  state.text += "[b]" + text + "[/b]"
  state.pos += 1

  return true
}

function italic_text(selection, state) {
  const { node } = state

  if (node.type !== "italic") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  state.text += "[i]" + text + "[/i]"
  state.pos += 1

  return true
}

function underline_text(selection, state) {
  const { node } = state

  if (node.type !== "underline") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  state.text += "[u]" + text + "[/u]"
  state.pos += 1

  return true
}

function strikethrough_text(selection, state) {
  const { node } = state

  if (node.type !== "strikethrough") {
    return false
  }

  const text = selection.renderNodes(node.children)
  if (!text) {
    return false
  }

  state.text += "[s]" + text + "[/s]"
  state.pos += 1

  return true
}

function inline_code(selection, state) {
  const { node } = state

  if (node.type !== "inline_code") {
    return false
  }

  const { content } = node
  if (!content) {
    return false
  }

  state.text += "`" + escapeInlineCode(content) + "`"
  state.pos += 1

  return true
}

function softbreak(selection, state) {
  const { node } = state

  if (node.type !== "softbreak") {
    return false
  }

  state.text += "\n"

  state.pos += 1
  return true
}

function text(selection, state) {
  const { node } = state

  if (node.type !== "text") {
    return false
  }

  // We rely on 'softbreak' rule for explicit line breaks
  state.text += node.content.replaceAll("\n", "")
  state.pos += 1

  return true
}

export default [
  { name: "attachment", func: attachment },
  { name: "youtube", func: youtube },
  { name: "header", func: header },
  { name: "quote", func: quote },
  { name: "code", func: code },
  { name: "spoiler", func: spoiler },
  { name: "paragraph", func: paragraph },
  { name: "table", func: table },
  { name: "list", func: list },
  { name: "hr", func: hr },
  { name: "image", func: image },
  { name: "link", func: link },
  { name: "strong_text", func: strong_text },
  { name: "emphasis_text", func: emphasis_text },
  { name: "bold_text", func: bold_text },
  { name: "italic_text", func: italic_text },
  { name: "underline_text", func: underline_text },
  { name: "strikethrough_text", func: strikethrough_text },
  { name: "inline_code", func: inline_code },
  { name: "softbreak", func: softbreak },
  { name: "text", func: text },
]
