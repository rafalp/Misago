import React from "react"

const useSearchQuery = (search: string, delay: number = 700) => {
  const s = search.trim().toLowerCase()
  const timeout = React.useRef<number>()
  const [filter, setFilter] = React.useState<string>(s)

  React.useEffect(() => {
    if (timeout.current) window.clearTimeout(timeout.current)

    if (s.length > 0) {
      timeout.current = window.setTimeout(() => {
        setFilter(s)
      }, delay)
    } else {
      setFilter("")
    }
  }, [s, delay, timeout, setFilter])

  return filter
}

export default useSearchQuery
