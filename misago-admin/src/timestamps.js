import $ from "jquery"
import moment from "moment"

const UI_UPDATE_INTERVAL = 20 * 1000 // 20 seconds
const RECENT_CUTOFF = 6 * 3600 // 6 hours

const initTimestamps = () => {
  const elements = document.querySelectorAll("[data-timestamp]")

  elements.forEach(setupTooltip)
  updateUITexts(elements)

  window.setInterval(() => {
    updateUITexts(elements)
  }, UI_UPDATE_INTERVAL)
}

const setupTooltip = element => {
  const date = moment(element.dataset.timestamp)
  element.title = date.format("LLLL")
  $(element).tooltip()
}

const updateUITexts = elements => {
  const now = moment()
  elements.forEach(element => {
    updateUIText(element, now)
  })
}

const updateUIText = (element, now) => {
  const date = moment(element.dataset.timestamp)
  const diff = Math.abs(date.diff(now, "seconds"))

  if (diff < RECENT_CUTOFF) {
    element.textContent = date.from(now)
  } else {
    const daysAgo = Math.abs(date.diff(now, "days"))
    if (daysAgo < 5) {
      element.textContent = date.calendar(now)
    } else {
      element.textContent = date.format(element.dataset.format)
    }
  }
}

export default initTimestamps
