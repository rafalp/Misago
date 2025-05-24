import getQuotedCode from "./getQuotedCode"

function attachment(selection, root, nodes) {
  const { ancestor } = root
  const container = ancestor.closest("[misago-rich-text-attachment]")

  if (!container) {
    return nodes
  }

  const args = container.getAttribute("misago-rich-text-attachment")

  return [
    {
      type: "attachment",
      args,
    },
  ]
}

function youtube(selection, root, nodes) {
  const { ancestor } = root
  const container = ancestor.closest("[misago-rich-text-youtube]")

  if (!container) {
    return nodes
  }

  const url = container.getAttribute("misago-rich-text-youtube")
  if (!url) {
    return nodes
  }

  return [
    {
      type: "youtube",
      url,
    },
  ]
}

function code(selection, root, nodes) {
  const { ancestor } = root
  const container = ancestor.closest("[misago-rich-text-code]")

  if (!container) {
    return nodes
  }

  const info = container.getAttribute("misago-rich-text-code")
  const content = getQuotedCode(root)

  return [
    {
      type: "code",
      info,
      content,
    },
  ]
}

function table(selection, root, nodes) {
  return nodes.map((node) => {
    if (node.type === "table") {
      return fixTable(selection, node)
    } else {
      return node
    }
  })
}

function fixTable(selection, table) {
  let result = fixTableHeader(selection, table)
  return fixTableColumns(selection, result)
}

function fixTableHeader(selection, table) {
  if (table.children[0].type === "table_head") {
    return table
  }

  const thead = {
    type: "table_head",
    children: [{ type: "table_row", children: [] }],
  }

  table.children = [thead, table.children[0]]

  return table
}

function fixTableColumns(selection, table) {
  const element = document
    .getElementById(table.children[1].children[0].id)
    .closest("table")

  const head = table.children[0]
  const body = table.children[1]

  const cols = {}
  head.children.forEach(function (row) {
    row.children.forEach(function (cell) {
      cols[cell.index] = true
    })
  })

  body.children.forEach(function (row) {
    row.children.forEach(function (cell) {
      cols[cell.index] = true
    })
  })

  head.children[0].children = selection.extractNodes(
    Array.from(element.querySelector("thead tr").childNodes)
      .filter((node) => node.nodeName === "TH")
      .filter((_, index) => cols[index])
  )

  body.children.forEach((row) => {
    row.children = selection.extractNodes(
      Array.from(document.getElementById(row.id).childNodes)
        .filter((node) => node.nodeName === "TD")
        .filter((_, index) => cols[index])
    )
  })

  return table
}

function table_head(selection, root, nodes) {
  if (!nodes || nodes[0].type !== "table_head") {
    return nodes
  }

  const table = root.ancestor.closest("table")

  const cols = {}
  nodes.forEach(function (rowset) {
    rowset.children.forEach(function (row) {
      row.children.forEach(function (cell) {
        cols[cell.index] = true
      })
    })
  })

  const thead = {
    type: "table_head",
    children: [
      {
        type: "table_row",
        children: selection.extractNodes(
          Array.from(table.querySelector("thead tr").childNodes)
            .filter((node) => node.nodeName === "TH")
            .filter((_, index) => cols[index])
        ),
      },
    ],
  }

  const tbody = {
    type: "table_body",
    children: nodes[1].children.map((row) => {
      row.children = selection.extractNodes(
        Array.from(document.getElementById(row.id).childNodes)
          .filter((node) => node.nodeName === "TD")
          .filter((_, index) => cols[index])
      )
      return row
    }),
  }

  return [
    {
      type: "table",
      children: [thead, tbody],
    },
  ]
}

function table_row(selection, root, nodes) {
  if (!nodes || nodes[0].type !== "table_row") {
    return nodes
  }

  const table = root.ancestor.closest("table")

  const cols = {}
  nodes.forEach(function (row) {
    row.children.forEach(function (cell) {
      cols[cell.index] = true
    })
  })

  const thead = {
    type: "table_head",
    children: [
      {
        type: "table_row",
        children: selection.extractNodes(
          Array.from(table.querySelector("thead tr").childNodes)
            .filter((node) => node.nodeName === "TH")
            .filter((_, index) => cols[index])
        ),
      },
    ],
  }

  const tbody = {
    type: "table_body",
    children: nodes.map((row) => {
      row.children = selection.extractNodes(
        Array.from(document.getElementById(row.id).childNodes)
          .filter((node) => node.nodeName === "TD")
          .filter((_, index) => cols[index])
      )
      return row
    }),
  }

  return [
    {
      type: "table",
      children: [thead, tbody],
    },
  ]
}

function table_th(selection, root, nodes) {
  if (!nodes || nodes[0].type !== "table_th") {
    return nodes
  }

  const cols = {}
  nodes.forEach(function (cell) {
    cols[cell.index] = true
  })

  const thead = {
    type: "table_head",
    children: [
      {
        type: "table_row",
        children: selection.extractNodes(
          Array.from(root.ancestor.closest("tr").childNodes)
            .filter((node) => node.nodeName === "TH")
            .filter((_, index) => cols[index])
        ),
      },
    ],
  }

  return [
    {
      type: "table",
      children: [thead],
    },
  ]
}

function table_td(selection, root, nodes) {
  if (!nodes || nodes[0].type !== "table_td") {
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

  const cols = {}
  nodes.forEach(function (cell) {
    cols[cell.index] = true
  })

  const tbody = {
    type: "table_body",
    children: [
      {
        type: "table_row",
        children: selection.extractNodes(
          Array.from(root.ancestor.closest("tr").childNodes)
            .filter((node) => node.nodeName === "TD")
            .filter((_, index) => cols[index])
        ),
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

function table_content(selection, root, nodes) {
  const td = root.ancestor.closest("td")

  if (!td) {
    return nodes
  }

  const table = root.ancestor.closest("table")
  const header = Array.from(table.querySelector("thead tr").childNodes).filter(
    (node) => node.nodeName === "TH"
  )

  const node = Object.assign(selection.extractNodes([td])[0], {
    children: nodes,
  })

  return [
    {
      type: "table",
      children: [
        {
          type: "table_head",
          children: [
            {
              type: "table_row",
              children: selection.extractNodes([header[node.index]]),
            },
          ],
        },
        {
          type: "table_body",
          children: [
            {
              type: "table_row",
              children: [node],
            },
          ],
        },
      ],
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

function blocks(selection, root, nodes) {
  let spoiler = false
  let quote = false

  let result = nodes

  let parent = root.ancestor
  while (!parent.hasAttribute("misago-quote-root")) {
    if (parent.hasAttribute("misago-rich-text-spoiler")) {
      spoiler = true
      result = [
        {
          type: "spoiler",
          info: parent.getAttribute("misago-rich-text-spoiler"),
          children: result,
        },
      ]
    } else if (parent.hasAttribute("misago-rich-text-quote")) {
      quote = true
      result = [
        {
          type: "quote",
          info: parent.getAttribute("misago-rich-text-quote"),
          children: result,
        },
      ]
    }

    if (spoiler && quote) {
      return result
    }

    parent = parent.parentNode
  }

  return result
}

function quote_wrapper(selection, root, nodes) {
  if (!nodes) {
    return false
  }

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
  if (nodes.length !== 1) {
    return true
  }

  if (nodes[0].type === "quote" && nodes[0].info) {
    return false
  }

  if (nodes[0].type === "spoiler") {
    return wrapNodesInQuote(nodes[0].children)
  }

  return true
}

export default [
  { name: "attachment", func: attachment },
  { name: "youtube", func: youtube },
  { name: "code", func: code },
  { name: "table", func: table },
  { name: "table_head", func: table_head },
  { name: "table_row", func: table_row },
  { name: "table_th", func: table_th },
  { name: "table_td", func: table_td },
  { name: "table_content", func: table_content },
  { name: "list", func: list },
  { name: "blocks", func: blocks },
  { name: "quote_wrapper", func: quote_wrapper },
]
