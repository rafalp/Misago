export const locale = window.misago_locale || "en-us"

export const momentAgo = pgettext("time ago", "moment ago")
export const momentAgoNarrow = pgettext("time ago", "now")
export const dayAt = pgettext("day at time", "%(day)s at %(time)s")
export const soonAt = pgettext("day at time", "at %(time)s")
export const tomorrowAt = pgettext("day at time", "Tomorrow at %(time)s")
export const yesterdayAt = pgettext("day at time", "Yesterday at %(time)s")

export const minuteShort = pgettext("short minutes", "%(time)sm")
export const hourShort = pgettext("short hours", "%(time)sh")
export const dayShort = pgettext("short days", "%(time)sd")
export const thisYearShort = pgettext("short month", "%(day)s %(month)s")
export const otherYearShort = pgettext("short month", "%(month)s %(year)s")

export const relativeNumeric = new Intl.RelativeTimeFormat(locale, {
  numeric: "always",
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

export const short = new Intl.DateTimeFormat(locale, {
  year: "2-digit",
  month: "short",
  day: "numeric",
})

export const weekday = new Intl.DateTimeFormat(locale, {
  weekday: "long",
})

export const shortTime = new Intl.DateTimeFormat(locale, { timeStyle: "short" })

export function formatShort(date) {
  const now = new Date()
  const absDiff = Math.abs(Math.round((date - now) / 1000))

  if (absDiff < 60) {
    return momentAgoNarrow
  }

  if (absDiff < 60 * 55) {
    const minutes = Math.ceil(absDiff / 60)
    return minuteShort.replace("%(time)s", minutes)
  }

  if (absDiff < 3600 * 24) {
    const hours = Math.ceil(absDiff / 3600)
    return hourShort.replace("%(time)s", hours)
  }

  if (absDiff < 86400 * 7) {
    const days = Math.ceil(absDiff / 86400)
    return dayShort.replace("%(time)s", days)
  }

  const parts = {}
  short.formatToParts(date).forEach(function ({ type, value }) {
    parts[type] = value
  })

  if (date.getFullYear() === now.getFullYear()) {
    return thisYearShort
      .replace("%(day)s", parts.day)
      .replace("%(month)s", parts.month)
  }

  return otherYearShort
    .replace("%(year)s", parts.year)
    .replace("%(month)s", parts.month)
}

export function formatRelative(date) {
  const now = new Date()
  const diff = Math.round((date - now) / 1000)
  const absDiff = Math.abs(diff)
  const sign = diff < 1 ? -1 : 1

  if (absDiff < 90) {
    return momentAgo
  }

  if (absDiff < 60 * 47) {
    const minutes = Math.ceil(absDiff / 60) * sign
    return relativeNumeric.format(minutes, "minute")
  }

  if (absDiff < 3600 * 3) {
    const hours = Math.ceil(absDiff / 3600) * sign
    return relativeNumeric.format(hours, "hour")
  }

  if (isSameDay(now, date)) {
    if (diff > 0) {
      return soonAt.replace("%(time)s", shortTime.format(date))
    }

    return shortTime.format(date)
  }

  if (isYesterday(date)) {
    return yesterdayAt.replace("%(time)s", shortTime.format(date))
  }

  if (isTomorrow(date)) {
    return tomorrowAt.replace("%(time)s", shortTime.format(date))
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
