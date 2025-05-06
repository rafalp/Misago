import getQuotedCode from "./getQuotedCode"

function code(selection, root, nodes) {
  const { ancestor } = root
  const container = ancestor.closest("[misago-code]")

  if (!container) {
    return nodes
  }

  const info = container.getAttribute("misago-code")
  const content = getQuotedCode(root)

  return [
    {
      type: "code",
      info,
      content,
    },
  ]
}

function table_td(selection, root, nodes) {
  if (nodes[0].type !== "table_td") {
    return nodes
  }

  const table = root.ancestor.closest("table")
  const header = Array.from(table.querySelector("thead tr").childNodes).filter(
    (node) => node.nodeName === "TH"
  )

  const thead = {
    type: "table_head",
    children: [{ type: "table_row", children: [] }],
  }

  nodes.forEach(function (node) {
    thead.children[0].children.push(
      selection.extractNodes([header[node.index]])[0]
    )
  })

  const tbody = {
    type: "table_body",
    children: [{ type: "table_row", children: nodes }],
  }

  return [
    {
      type: "table",
      children: [thead, tbody],
    },
  ]
}

function list(selection, root, nodes) {
  if (root.ancestor.nodeName === "OL" || root.ancestor.nodeName === "UL") {
    return [
      {
        type: "list",
        ordered: root.ancestor.nodeName === "OL",
        children: nodes,
      },
    ]
  }

  return nodes
}

function spoiler(selection, root, nodes) {
  const { ancestor } = root
  const container = ancestor.closest("[misago-spoiler]")

  if (!container) {
    return nodes
  }

  const info = container.getAttribute("misago-spoiler")

  return [
    {
      type: "spoiler",
      info,
      children: nodes,
    },
  ]
}

function quote(selection, root, nodes) {
  if (!wrapNodesInQuote(nodes)) {
    return nodes
  }

  return [
    {
      type: "quote",
      info: root.info,
      children: nodes,
    },
  ]
}

function wrapNodesInQuote(nodes) {
  if (nodes.length === 1 && nodes[0].type === "quote") {
    return false
  }

  if (nodes.length === 1 && nodes[0].type === "spoiler") {
    return wrapNodesInQuote(nodes[0].children)
  }

  return true
}

export default [
  { name: "code", func: code },
  { name: "table_td", func: table_td },
  { name: "list", func: list },
  { name: "spoiler", func: spoiler },
  { name: "quote", func: quote },
]
