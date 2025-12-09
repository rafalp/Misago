import htmx from "htmx.org"

function onEvent(name, event) {
  if (name === "htmx:beforeRequest") {
    const options = getModalOptions(event)
    if (options) {
      onModalBeforeRequest(event, options)
    }
  }
}

function getModalOptions(event) {
  if (!event.target) {
    return null
  }

  const swap = getClosestAttribute(event.target, "hx-swap")
  if (swap !== null && swap !== "innerHTML") {
    console.warn(
      "'hx-swap' attribute for modal target must be 'innerHTML' or not set."
    )
    return null
  }

  const modalSelector = getClosestAttribute(event.target, "mg-modal")
  if (!modalSelector) {
    console.warn("Could not resolve the 'mg-modal' attribute.")
    return null
  }

  const modal = document.querySelector(modalSelector)
  if (!modal) {
    console.warn(
      "Could not resolve the '" +
        modalSelector +
        "' element specified in the 'mg-modal' attribute."
    )
    return null
  }

  const modalTitle = getClosestAttribute(event.target, "mg-modal-title")
  let modalTitleElement = null
  if (modalTitle) {
    modalTitleElement = modal.querySelector("[mg-modal-title]")
    if (!modalTitleElement) {
      console.warn(
        "Could not resolve the 'mg-modal-title' child element for modal."
      )
      return null
    }
  }

  const loaderSelector = getClosestAttribute(event.target, "mg-modal-loader")
  let loader = loaderSelector ? document.querySelector(loaderSelector) : null
  if (loaderSelector && !loader) {
    console.warn(
      "Could not resolve the '" +
        loaderSelector +
        "' element specified in the 'mg-modal-loader' attribute."
    )
    return null
  }

  return {
    modal,
    loader,
    selector: modalSelector,
    title: modalTitle ? { text: modalTitle, element: modalTitleElement } : null,
  }
}

function getClosestAttribute(element, attr) {
  const el = element.closest("[" + attr + "]")
  if (el) {
    return el.getAttribute(attr)
  }
  return null
}

function onModalBeforeRequest(event, options) {
  if (options.title) {
    options.title.element.textContent = options.title.text
  }

  console.log(options)
  if (options.loader) {
    event.detail.target.replaceChildren(options.loader.content.cloneNode(true))
  }

  $(options.selector).modal("show")
}

htmx.defineExtension("mg-modal", { onEvent })

function preventDefault(event) {
  event.preventDefault()
}

htmx.onLoad(function () {
  document.querySelectorAll("[mg-modal]").forEach(function (element) {
    element.addEventListener("click", preventDefault)
  })
})
