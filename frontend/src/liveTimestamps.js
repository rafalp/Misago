import htmx from "htmx.org"

import { formatRelative, formatShort, fullDateTime } from "./datetimeFormats"

const cache = {}

export function updateTimestamp(element) {
  const timestamp = element.getAttribute("misago-timestamp")
  if (!cache[timestamp]) {
    cache[timestamp] = new Date(timestamp)
  }

  if (!element.hasAttribute("title")) {
    element.setAttribute("title", fullDateTime.format(cache[timestamp]))
  }

  const format = element.getAttribute("misago-timestamp-format")

  if (format == "short") {
    element.textContent = formatShort(cache[timestamp])
  } else {
    element.textContent = formatRelative(cache[timestamp])
  }
}

export function startLiveTimestamps() {
  document.querySelectorAll("[misago-timestamp]").forEach(updateTimestamp)

  updateLiveTimestamps()
  window.setInterval(updateLiveTimestamps, 1000 * 55)
}

export function updateLiveTimestamps(element) {
  const target = element || document
  target.querySelectorAll("[misago-timestamp]").forEach(updateTimestamp)
}

startLiveTimestamps()
htmx.onLoad(updateLiveTimestamps)
