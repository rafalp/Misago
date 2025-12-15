import htmx from "htmx.org"
import { getClosestAttribute } from "./closest-attribute"

function onEvent(name, event) {
  if (name === "htmx:beforeSend") {
    const options = getModalOptions(event)
    if (options) {
      onModalBeforeSend(event, options)
    }
  }
}

function getModalOptions(event) {
  if (!event.target) {
    return null
  }

  const swap = getClosestAttribute(event.target, "hx-swap")
  if (!!swap && swap !== "innerHTML") {
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

  return {
    modal,
    selector: modalSelector,
    title: modalTitle ? { text: modalTitle, element: modalTitleElement } : null,
  }
}

function onModalBeforeSend(event, options) {
  if (options.title) {
    options.title.element.textContent = options.title.text
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
