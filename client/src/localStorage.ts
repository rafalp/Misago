import React from "react"

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

interface IStorageEventData {
  newValue: string | null
  oldValue: string | null
}

const useStorageEvent = (key: string): IStorageEventData | undefined => {
  const [state, updateState] = React.useState<IStorageEventData | undefined>(
    undefined
  )
  React.useEffect(() => {
    const prefixedKey = prefix + key
    const handler = ({ key, newValue, oldValue }: StorageEvent) => {
      if (key !== prefixedKey) return
      updateState({ newValue, oldValue })
    }

    window.addEventListener("storage", handler)
    return () => window.removeEventListener("storage", handler)
  }, [key])

  return state
}

export { prefix, getItem, removeItem, setItem, useStorageEvent }
