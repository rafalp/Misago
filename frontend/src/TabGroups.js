import htmx from "htmx.org"

function updateTabGroups(hash) {
  if (!hash) {
    return
  }

  document.querySelectorAll(".tab-group").forEach(function (element) {
    updateTabGroup(hash, element)
  })
}

function updateTabGroup(hash, element) {
  let oldNav = null
  let newNav = null

  element.querySelectorAll(".tab-group-nav a").forEach(function (nav) {
    if (nav.getAttribute("href") === hash) {
      newNav = nav
    }
    if (nav.classList.contains("active")) {
      oldNav = nav
    }
  })

  const oldTab = element.querySelector(".tab-group-tab.visible")
  const newTab = findTab(hash.substring(1), element)

  if (newNav && newTab && newNav != oldNav && newTab !== oldTab) {
    newNav.classList.add("active")
    newTab.classList.add("visible")

    if (oldNav) {
      oldNav.classList.remove("active")
    }

    if (oldTab) {
      oldTab.classList.remove("visible")
    }

    const event = new CustomEvent("misago:updated-tab", {
      bubbles: true,
      target: element,
      oldTab,
      newTab,
    })
    element.dispatchEvent(event)
  }
}

function findTab(hash, element) {
  const tabs = element.querySelectorAll("[misago-tab-group-tab]")
  for (let i = 0; i < tabs.length; i++) {
    const tab = tabs[i]
    if (tab.getAttribute("misago-tab-group-tab") === hash) {
      return tab
    }
  }
  return null
}

window.addEventListener("hashchange", function () {
  updateTabGroups(window.location.hash)
})

htmx.onLoad(function () {
  updateTabGroups(window.location.hash)
})

export { updateTabGroups }
