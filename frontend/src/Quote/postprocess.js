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
  if (nodes.length === 1 && nodes[0].type === "quote") {
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

export default [
  { name: "code", func: code },
  { name: "list", func: list },
  { name: "spoiler", func: spoiler },
  { name: "quote", func: quote },
]
