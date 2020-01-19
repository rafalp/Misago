const WINDOW_KEY = "__misago_prefix"

const prefix = String((window as any)[WINDOW_KEY] || "__")

const setItem = (key: string, value: string): string => {
  window.localStorage.setItem(prefix + key, value)
  return value
}

const getItem = (
  key: string,
  default_: string | null = null
): string | null => {
  const value = window.localStorage.getItem(prefix + key)
  if (value === null) return default_
  return value
}

const removeItem = (key: string) => {
  window.localStorage.removeItem(prefix + key)
}

export { prefix, getItem, removeItem, setItem }
