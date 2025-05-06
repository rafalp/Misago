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

function table_thead(selection, root, nodes) {
  if (nodes[0].type !== "table_thead") {
    return nodes
  }

  const thead = {
    type: "table_head",
    children: [{ type: "table_row", children: nodes }],
  }

  const tbody = {
    type: "table_body",
    children: [],
  }

  return [
    {
      type: "table",
      children: [thead, tbody],
    },
  ]
}

function table_row(selection, root, nodes) {
  if (nodes[0].type !== "table_row") {
    return nodes
  }

  const table = root.ancestor.closest("table")
  const header = selection.extractNodes(
    Array.from(table.querySelector("thead tr").childNodes).filter(
      (node) => node.nodeName === "TH"
    )
  )

  const cols = {}
  nodes.forEach(function (row) {
    row.children.forEach(function (cell) {
      cols[cell.index] = true
    })
  })

  const length = Object.keys(cols).length

  const thead = {
    type: "table_head",
    children: [{ type: "table_row", children: [] }],
  }

  header.forEach(function (node, index) {
    if (cols[index]) {
      thead.children[0].children.push(header[index])
    }
  })

  const tbody = {
    type: "table_body",
    children: [],
  }

  const blankCell = {
    type: "table_td",
    index: null,
    alignment: null,
    children: [{ type: "text", content: "" }],
  }

  nodes.forEach(function (rowNode) {
    const children = []

    for (let index = 0; index < rowNode.children[0].index; index++) {
      if (cols[index]) {
        children.push(blankCell)
      }
    }

    rowNode.children.forEach(function (node) {
      children.push(node)
    })

    while (children.length < length) {
      children.push(blankCell)
    }

    tbody.children.push({
      type: "table_row",
      children,
    })
  })

  return [
    {
      type: "table",
      children: [thead, tbody],
    },
  ]
}

function table_th(selection, root, nodes) {
  if (nodes[0].type !== "table_th") {
    return nodes
  }

  const thead = {
    type: "table_head",
    children: [{ type: "table_row", children: nodes }],
  }

  const tbody = {
    type: "table_body",
    children: [
      {
        type: "table_row",
        children: nodes.map(function () {
          return {
            type: "table_td",
            children: [{ type: "text", content: "" }],
          }
        }),
      },
    ],
  }

  return [
    {
      type: "table",
      children: [thead, tbody],
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
  { name: "table_thead", func: table_thead },
  { name: "table_row", func: table_row },
  { name: "table_th", func: table_th },
  { name: "table_td", func: table_td },
  { name: "list", func: list },
  { name: "spoiler", func: spoiler },
  { name: "quote", func: quote },
]
