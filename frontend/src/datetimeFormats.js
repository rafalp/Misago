export const locale = window.misago_locale || "en-us"
export const momentAgo = pgettext("moment", "moment ago")
export const dayAt = pgettext("day at time", "%(day)s at %(time)s")

export const relativeNumeric = new Intl.RelativeTimeFormat(locale, {
  numeric: "always",
  style: "long",
})

export const relativeAuto = new Intl.RelativeTimeFormat(locale, {
  numeric: "auto",
  style: "long",
})

export const fullDateTime = new Intl.DateTimeFormat(locale, {
  dateStyle: "full",
  timeStyle: "medium",
})

export const thisYearDate = new Intl.DateTimeFormat(locale, {
  month: "long",
  day: "numeric",
})

export const otherYearDate = new Intl.DateTimeFormat(locale, {
  year: "numeric",
  month: "long",
  day: "numeric",
})

export const weekday = new Intl.DateTimeFormat(locale, {
  weekday: "long",
})

export const shortTime = new Intl.DateTimeFormat(locale, { timeStyle: "short" })

export function formatRelative(date) {
  const now = new Date()
  const diff = Math.round((date - now) / 1000)
  const absDiff = Math.abs(diff)

  if (absDiff < 90) {
    return momentAgo
  }

  if (absDiff < 60 * 47) {
    const minutes = Math.ceil(diff / 60)
    return relativeNumeric.format(minutes, "minute")
  }

  if (absDiff < 3600 * 3) {
    const hours = Math.ceil(diff / 3600)
    return relativeNumeric.format(hours, "hour")
  }

  if (isSameDay(now, date)) {
    return shortTime.format(date)
  }

  if (isYesterday(date)) {
    const yesterday = relativeAuto.formatToParts(-1, "day")[0].value
    return formatDayAtTime(yesterday, date)
  }

  if (isTomorrow(date)) {
    const tomorrow = relativeAuto.formatToParts(1, "day")[0].value
    return formatDayAtTime(tomorrow, date)
  }

  if (diff < 0 && absDiff < 3600 * 24 * 6) {
    const day = weekday.format(date)
    return formatDayAtTime(day, date)
  }

  if (now.getFullYear() == date.getFullYear()) {
    return thisYearDate.format(date)
  }

  return otherYearDate.format(date)
}

export function isSameDay(now, date) {
  return (
    now.getFullYear() == date.getFullYear() &&
    now.getMonth() == date.getMonth() &&
    now.getDate() == date.getDate()
  )
}

export function isYesterday(date) {
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  return isSameDay(yesterday, date)
}

export function isTomorrow(date) {
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() + 1)
  return isSameDay(yesterday, date)
}

export function formatDayAtTime(day, date) {
  return dayAt
    .replace("%(day)s", day)
    .replace("%(time)s", shortTime.format(date))
}
