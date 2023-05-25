export const locale = window.misago_locale || "en-us"

export const momentAgo = pgettext("time ago", "moment ago")
export const momentAgoNarrow = pgettext("time ago", "now")
export const dayAt = pgettext("day at time", "%(day)s at %(time)s")
export const tomorrowAt = pgettext("day at time", "Tomorrow at %(time)s")
export const yesterdayAt = pgettext("day at time", "Yesterday at %(time)s")

export const minuteCompact = pgettext("short minutes", "%(time)sm")
export const hourCompact = pgettext("short hours", "%(time)sh")
export const dayCompact = pgettext("short days", "%(time)sd")

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

export const thisYearDateNarrow = new Intl.DateTimeFormat(locale, {
  month: "short",
  day: "numeric",
})

export const otherYearDate = new Intl.DateTimeFormat(locale, {
  year: "numeric",
  month: "long",
  day: "numeric",
})

export const otherYearDateNarrow = new Intl.DateTimeFormat(locale, {
  year: "2-digit",
  month: "short",
})

export const weekday = new Intl.DateTimeFormat(locale, {
  weekday: "long",
})

export const shortTime = new Intl.DateTimeFormat(locale, { timeStyle: "short" })

export function formatNarrow(date) {
  const now = new Date()
  const absDiff = Math.abs(Math.round((date - now) / 1000))

  if (absDiff < 60) {
    return momentAgoNarrow
  }

  if (absDiff < 60 * 55) {
    const minutes = Math.ceil(absDiff / 60)
    return minuteCompact.replace("%(time)s", minutes)
  }

  if (absDiff < 3600 * 24) {
    const hours = Math.ceil(absDiff / 3600)
    return hourCompact.replace("%(time)s", hours)
  }

  if (absDiff < 86400 * 7) {
    const days = Math.ceil(absDiff / 86400)
    return dayCompact.replace("%(time)s", days)
  }

  if (date.getFullYear() === now.getFullYear()) {
    return thisYearDateNarrow.format(date)
  }

  return otherYearDateNarrow.format(date)
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
