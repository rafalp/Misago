import htmx from "htmx.org"

import {
  dateRelative,
  dateRelativeInSentence,
  dateRelativeShort,
  fullDateTime,
} from "./formats"

const cache = {}

export function updateTimestamp(element) {
  const timestamp =
    element.getAttribute("mg-timestamp") ||
    element.getAttribute("misago-timestamp")
  const format =
    element.getAttribute("mg-timestamp-format") ||
    element.getAttribute("misago-timestamp-format")

  if (!cache[timestamp]) {
    cache[timestamp] = new Date(timestamp)
  }

  if (format !== "full" && !element.hasAttribute("mg-timestamp-title")) {
    element.setAttribute("mg-timestamp-title", "true")
    element.setAttribute("title", fullDateTime.format(cache[timestamp]))
  }

  if (format === "short") {
    element.textContent = dateRelativeShort(cache[timestamp])
  } else if (format === "full") {
    element.textContent = fullDateTime.format(cache[timestamp])
  } else if (format === "sentence") {
    element.textContent = dateRelativeInSentence(cache[timestamp])
  } else {
    element.textContent = dateRelative(cache[timestamp])
  }
}

export function startTimestampsUpdates() {
  document
    .querySelectorAll("[mg-timestamp],[misago-timestamp]")
    .forEach(updateTimestamp)

  updateTimestamps()
  window.setInterval(updateTimestamps, 1000 * 55)
}

export function updateTimestamps(element) {
  const target = element || document
  target
    .querySelectorAll("[mg-timestamp],[misago-timestamp]")
    .forEach(updateTimestamp)
}

startTimestampsUpdates()
htmx.onLoad(updateTimestamps)
