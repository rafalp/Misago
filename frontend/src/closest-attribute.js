function getClosestAttribute(target, name, default_) {
  const element = target.closest("[" + name + "]")
  if (!element) {
    return default_ || undefined
  }

  return element.getAttribute(name) || default_ || undefined
}

function getClosestBoolAttribute(target, name, default_) {
  const attribute = getClosestAttribute(target, name)
  if (attribute === "false") {
    return false
  }
  if (attribute === "true") {
    return true
  }
  return default_
}

export { getClosestAttribute, getClosestBoolAttribute }
