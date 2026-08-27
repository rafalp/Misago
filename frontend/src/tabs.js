import htmx from "htmx.org"

function updateTabs(hash) {
  if (!hash) {
    return
  }

  document.querySelectorAll("[m-tabs]").forEach(function (element) {
    updateTabsElement(hash, element)
  })
}

function updateTabsElement(hash, target) {
  let oldTab = null
  let newTab = null

  target.querySelectorAll("[m-tab]").forEach(function (nav) {
    if (nav.getAttribute("href") === hash) {
      newTab = nav
    }
    if (nav.classList.contains("active")) {
      oldTab = nav
    }
  })

  const oldPane = target.querySelector("[m-tab-pane].active")
  const newPane = findPane(hash.substring(1), target)

  if (newTab && newPane && newTab != oldTab && newPane !== oldPane) {
    newTab.classList.add("active")
    newPane.classList.add("active")
    console.log(newPane)

    if (oldTab) {
      oldTab.classList.remove("active")
    }

    if (oldPane) {
      oldPane.classList.remove("active")
    }

    const event = new CustomEvent("misago:updated-tab", {
      bubbles: true,
      target: target,
      oldPane,
      newPane,
    })
    target.dispatchEvent(event)
  }
}

function findPane(hash, target) {
  const panes = target.querySelectorAll("[m-tab-pane]")
  for (let i = 0; i < panes.length; i++) {
    const pane = panes[i]
    if (pane.getAttribute("m-tab-pane") === hash) {
      return pane
    }
  }
  return null
}

window.addEventListener("hashchange", function () {
  updateTabs(window.location.hash)
})

htmx.onLoad(function () {
  updateTabs(window.location.hash)
})

export { updateTabs }
