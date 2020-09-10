import React from "react"
import { ICategoryChoice } from "../PostThread.types"

const useSearchQuery = (search: string, delay: number = 700) => {
  const s = search.trim().toLowerCase()
  const timeout = React.useRef<number>()
  const [filter, setFilter] = React.useState<string>(s)

  React.useEffect(() => {
    if (timeout.current) window.clearTimeout(timeout.current)

    if (s.length > 0) {
      timeout.current = window.setTimeout(() => {
        setFilter(s)
      }, 700)
    } else {
      setFilter("")
    }
  }, [s, timeout, setFilter])

  return filter
}

const useFilteredChoices = (
  choices: Array<ICategoryChoice>,
  search: string
) => {
  const query = useSearchQuery(search)

  return React.useMemo(() => {
    if (query.trim().length === 0) {
      return choices
    }

    const results = choices.map((category) => {
      const foundChildren = category.children.filter((child) => {
        return child.name.toLowerCase().indexOf(query) >= 0
      })

      if (
        category.name.toLowerCase().indexOf(query) >= 0 ||
        foundChildren.length
      ) {
        return Object.assign({}, category, { children: foundChildren })
      }

      return null
    })

    return results.filter((result) => {
      return result !== null
    }) as Array<ICategoryChoice>
  }, [choices, query])
}

export default useFilteredChoices
