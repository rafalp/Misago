import { formatRelative, fullDateTime } from "./datetimeFormats"

const cache = {}

export function startLiveTimestamps() {
  document.querySelectorAll("[misago-timestamp]").forEach((element) => {
    const timestamp = element.getAttribute("misago-timestamp")
    if (!cache[timestamp]) {
      cache[timestamp] = new Date(timestamp)
    }

    if (!element.hasAttribute("title")) {
      element.setAttribute("title", fullDateTime.format(cache[timestamp]))
    }

    element.textContent = formatRelative(cache[timestamp])
  })

  updateLiveTimestamps()
  window.setInterval(updateLiveTimestamps, 1000 * 55)
}

export function updateLiveTimestamps() {
  document.querySelectorAll("[misago-timestamp]").forEach((element) => {
    const timestamp = element.getAttribute("misago-timestamp")
    if (!cache[timestamp]) {
      cache[timestamp] = new Date(timestamp)
    }

    element.textContent = formatRelative(cache[timestamp])
  })
}
