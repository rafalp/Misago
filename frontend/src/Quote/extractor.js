import getQuotedCode from "./getQuotedCode"

function attachment(selection, state) {
  const { result, node } = state

  if (node.nodeName !== "DIV" && node.nodeName !== "SPAN") {
    return false
  }

  const attachment = node.getAttribute("misago-rich-text-attachment")
  if (!attachment) {
    return false
  }

  if (!node.childNodes.length) {
    return false
  }

  result.push({
    type: "attachment",
    args: attachment,
  })

  state.pos += 1
  return true
}

function youtube(selection, state) {
  const { result, node } = state

  if (node.nodeName !== "DIV") {
    return false
  }

  const url = node.getAttribute("misago-rich-text-youtube")
  if (!url) {
    return false
  }

  result.push({
    type: "youtube",
    url,
  })

  state.pos += 1
  return true
}

const HEADER_NODES = {
  H1: true,
  H2: true,
  H3: true,
  H4: true,
  H5: true,
  H6: true,
}

function header(selection, state) {
  const { result, node, stack } = state

  if (!HEADER_NODES[node.nodeName]) {
    return false
  }

  const children = selection.extractNodes(
    node.childNodes,
    stack.concat(["header"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  const level = parseInt(node.nodeName.substring(1))

  result.push({
    type: "header",
    level,
    children,
  })

  state.pos += 1
  return true
}

function quote(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "ASIDE") {
    return false
  }

  const blockquote = node.querySelector("blockquote[misago-rich-text-quote]")
  if (!blockquote) {
    return false
  }

  const info = blockquote.getAttribute("misago-rich-text-quote")

  const children = selection.extractNodes(
    blockquote.childNodes,
    stack.concat(["quote"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  result.push({
    type: "quote",
    info,
    children,
  })

  state.pos += 1
  return true
}

function spoiler(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "DETAILS") {
    return false
  }

  const body = node.querySelector("div[misago-rich-text-spoiler]")
  if (!body) {
    return false
  }

  const info = body.getAttribute("misago-rich-text-spoiler")

  const children = selection.extractNodes(
    body.childNodes,
    stack.concat(["quote"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  result.push({
    type: "spoiler",
    info,
    children,
  })

  state.pos += 1
  return true
}

function code(selection, state) {
  const { result, node, stack } = state

  if (!(node.nodeName === "DIV" || node.nodeName === "PRE")) {
    return false
  }

  const code = node.querySelector("code[misago-rich-text-code]")
  if (!code) {
    return false
  }

  const info = code.getAttribute("misago-rich-text-code")
  const content = getQuotedCode(code)

  result.push({
    type: "code",
    info,
    content,
  })

  state.pos += 1
  return true
}

function paragraph(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "P") {
    return false
  }

  const children = selection.extractNodes(
    node.childNodes,
    stack.concat(["paragraph"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  result.push({
    type: "paragraph",
    children,
  })

  state.pos += 1
  return true
}

function table(selection, state) {
  const { result, node, stack } = state

  if (
    node.nodeName !== "DIV" ||
    node.getAttribute("misago-rich-text") !== "table-container"
  ) {
    return false
  }

  const tables = Array.from(node.childNodes).filter(function (node) {
    return node.nodeName === "TABLE"
  })

  if (tables.length !== 1) {
    return false
  }

  const table = tables[0]

  const children = selection.extractNodes(
    table.childNodes,
    stack.concat(["table"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  result.push({
    type: "table",
    children,
  })

  state.pos += 1
  return true
}

function table_head(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "THEAD") {
    return false
  }

  const children = selection.extractNodes(
    node.childNodes,
    stack.concat(["table_head"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  result.push({
    type: "table_head",
    children,
  })

  state.pos += 1
  return true
}

function table_body(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "TBODY") {
    return false
  }

  const children = selection.extractNodes(
    node.childNodes,
    stack.concat(["table_body"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  result.push({
    type: "table_body",
    children,
  })

  state.pos += 1
  return true
}

function table_row(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "TR") {
    return false
  }

  const children = selection.extractNodes(
    node.childNodes,
    stack.concat(["table_row"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  result.push({
    type: "table_row",
    id: node.id,
    children,
  })

  state.pos += 1
  return true
}

function table_th(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "TH") {
    return false
  }

  const children = selection.extractNodes(
    node.childNodes,
    stack.concat(["table_th"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  const { index, alignment } = getTableCellMeta(node)

  result.push({
    type: "table_th",
    index,
    alignment,
    children,
  })

  state.pos += 1
  return true
}

function table_td(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "TD") {
    return false
  }

  const children = selection.extractNodes(
    node.childNodes,
    stack.concat(["table_td"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  const { index, alignment } = getTableCellMeta(node)

  result.push({
    type: "table_td",
    index,
    alignment,
    children,
  })

  state.pos += 1
  return true
}

function getTableCellMeta(node) {
  const meta = node.getAttribute("misago-rich-text-col")
  if (!meta) {
    return { index: null, alignment: "c" }
  }

  const values = meta.split(":")
  return { index: parseInt(values[0] || "0"), alignment: values[1] || "c" }
}

function list(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "OL" && node.nodeName !== "UL") {
    return false
  }

  const ordered = node.nodeName === "OL"

  const children = selection.extractNodes(
    node.childNodes,
    stack.concat(["list"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  result.push({
    type: "list",
    ordered,
    children,
  })

  state.pos += 1
  return true
}

function list_item(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "LI") {
    return false
  }

  const children = selection.extractNodes(
    node.childNodes,
    stack.concat(["list_item"])
  )

  if (!children.length) {
    state.pos += 1
    return true
  }

  result.push({
    type: "list_item",
    children,
  })

  state.pos += 1
  return true
}

function hr(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "HR") {
    return false
  }

  result.push({
    type: "hr",
  })

  state.pos += 1
  return true
}

function image(selection, state) {
  const { result, node } = state

  if (node.nodeName !== "IMG") {
    return false
  }

  const url = (node.getAttribute("src") || "").trim()
  const alt = (node.getAttribute("alt") || "").trim() || null
  const title = (node.getAttribute("title") || "").trim() || null

  if (!url) {
    return false
  }

  result.push({
    type: "image",
    url,
    alt,
    title,
  })

  state.pos += 1
  return true
}

function mention(selection, state) {
  const { result, node } = state

  if (!(node.nodeName === "A" || node.nodeName === "SPAN")) {
    return false
  }

  if (!node.getAttribute("misago-rich-text-mention")) {
    return false
  }

  result.push({
    type: "text",
    content: node.textContent,
  })

  state.pos += 1
  return true
}

function link(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "A") {
    return false
  }

  result.push({
    type: "link",
    href: node.getAttribute("href"),
    auto: node.getAttribute("misago-rich-text") === "autolink",
    children: selection.extractNodes(node.childNodes, stack.concat(["link"])),
  })

  state.pos += 1
  return true
}

function strong_text(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "STRONG") {
    return false
  }

  result.push({
    type: "strong",
    children: selection.extractNodes(
      node.childNodes,
      stack.concat(["strong_text"])
    ),
  })

  state.pos += 1
  return true
}

function emphasis_text(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "EM") {
    return false
  }

  result.push({
    type: "emphasis",
    children: selection.extractNodes(
      node.childNodes,
      stack.concat(["emphasis_text"])
    ),
  })

  state.pos += 1
  return true
}

function bold_text(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "B") {
    return false
  }

  result.push({
    type: "bold",
    children: selection.extractNodes(
      node.childNodes,
      stack.concat(["bold_text"])
    ),
  })

  state.pos += 1
  return true
}

function italic_text(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "I") {
    return false
  }

  result.push({
    type: "italic",
    children: selection.extractNodes(
      node.childNodes,
      stack.concat(["italic_text"])
    ),
  })

  state.pos += 1
  return true
}

function underline_text(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "U") {
    return false
  }

  result.push({
    type: "underline",
    children: selection.extractNodes(
      node.childNodes,
      stack.concat(["underline_text"])
    ),
  })

  state.pos += 1
  return true
}

function strikethrough_text(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "DEL") {
    return false
  }

  result.push({
    type: "strikethrough",
    children: selection.extractNodes(
      node.childNodes,
      stack.concat(["strikethrough_text"])
    ),
  })

  state.pos += 1
  return true
}

function inline_code(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "CODE") {
    return false
  }

  result.push({
    type: "inline_code",
    content: node.textContent,
  })

  state.pos += 1
  return true
}

function softbreak(selection, state) {
  const { result, node, stack } = state

  if (node.nodeName !== "BR") {
    return false
  }

  result.push({
    type: "softbreak",
  })

  state.pos += 1
  return true
}

function text(selection, state) {
  const { result, node, stack } = state

  if (node.nodeType !== Node.TEXT_NODE) {
    return false
  }

  if (node.textContent === "\n") {
    state.pos += 1
    return true
  }

  result.push({
    type: "text",
    content: node.textContent,
  })

  state.pos += 1
  return true
}

export default [
  { name: "attachment", func: attachment },
  { name: "youtube", func: youtube },
  { name: "header", func: header },
  { name: "quote", func: quote },
  { name: "spoiler", func: spoiler },
  { name: "code", func: code },
  { name: "paragraph", func: paragraph },
  { name: "table", func: table },
  { name: "table_head", func: table_head },
  { name: "table_body", func: table_body },
  { name: "table_row", func: table_row },
  { name: "table_th", func: table_th },
  { name: "table_td", func: table_td },
  { name: "list", func: list },
  { name: "list_item", func: list_item },
  { name: "hr", func: hr },
  { name: "image", func: image },
  { name: "mention", func: mention },
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
