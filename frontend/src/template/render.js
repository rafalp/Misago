import { evaluateTemplateCondition } from "./condition"

function mountTemplate(root, template, context) {
  const rendered = renderTemplate(template, context)
  root.replaceChildren(rendered)
}

function renderTemplate(template, context) {
  const src = template.content.cloneNode(true)
  const children = Array.from(src.childNodes)
  for (let i = 0; i < children.length; i++) {
    if (children[i].tagName) {
      renderTemplateNode(children[i], context)
    }
  }

  return src
}

function renderTemplateNode(node, context) {
  if (node.hasAttribute("mg-if")) {
    const condition = node.getAttribute("mg-if").trim()
    if (evaluateTemplateCondition(condition, context)) {
      node.removeAttribute("mg-if")
    } else {
      node.remove()
    }
  }

  if (node.hasAttribute("mg-text")) {
    const name = node.getAttribute("mg-text").trim()
    node.removeAttribute("mg-text")
    if (name) {
      node.textContent = context[name] || ""
    }
  }

  if (node.childNodes.length) {
    const children = Array.from(node.childNodes)
    for (let i = 0; i < children.length; i++) {
      if (children[i].tagName) {
        renderTemplateNode(children[i], context)
      }
    }
  }
}

export { mountTemplate, renderTemplate }
