export default function renderTemplate(template, data) {
  const node = template.content.cloneNode(true)

  node.querySelectorAll("[misago-tpl-if]").forEach((element) => {
    const variable = element.getAttribute("misago-tpl-if")
    if (getVariableValue(data, variable)) {
      element.removeAttribute("misago-tpl-if")
    } else {
      element.remove()
    }
  })

  node.querySelectorAll("[misago-tpl-ifnot]").forEach((element) => {
    const variable = element.getAttribute("misago-tpl-ifnot")
    if (getVariableValue(data, variable)) {
      element.remove()
    } else {
      element.removeAttribute("misago-tpl-ifnot")
    }
  })

  node.querySelectorAll("[misago-tpl-var]").forEach((element) => {
    const variable = element.getAttribute("misago-tpl-var")
    element.innerText = getVariableValue(data, variable) || ""
    element.removeAttribute("misago-tpl-var")
  })

  node.querySelectorAll("[misago-tpl-attr]").forEach((element) => {
    const attr = element.getAttribute("misago-tpl-attr")
    if (attr.indexOf(":") !== ":") {
      const name = attr.substring(0, attr.indexOf(":")).trim()
      const variable = attr.substring(attr.indexOf(":") + 1).trim()
      const value = variable ? getVariableValue(data, variable) : undefined

      if (name && value) {
        element.setAttribute(name, value)
      }
    }
    element.removeAttribute("misago-tpl-attr")
  })

  return node
}

function getVariableValue(data, variable) {
  if (variable.indexOf(".") === -1) {
    return data[variable]
  } else {
    let value = data
    for (const part of variable.split(".")) {
      if (part && typeof value[part] !== "undefined") {
        value = value[part]
      } else {
        return undefined
      }
    }
    return value
  }
}
