const fullDate = {
  weekday: "long",
  year: "numeric",
  month: "long",
  day: "numeric",
  hour: "numeric",
  minute: "numeric",
  second: "numeric",
}

const shortDate = {
  year: "numeric",
  month: "long",
  day: "numeric",
}

export const formatDate = (date: Date, locale: string): string => {
  return date.toLocaleString(locale, fullDate)
}

export const formatDateShort = (date: Date, locale: string): string => {
  return date.toLocaleString(locale, shortDate)
}
