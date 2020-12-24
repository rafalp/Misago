import React from "react"

interface Selection<TSelectable extends { id: string }> {
  selection: Record<string, boolean>
  selected: Array<TSelectable>
  change: (id: string, selected: boolean) => void
  clear: () => void
  toggle: (id: string) => void
}

const useSelection = <TSelectable extends { id: string }>(
  items?: Array<TSelectable>,
  initial?: Array<TSelectable>
): Selection<TSelectable> => {
  const [selection, setState] = React.useState<Record<string, boolean>>(
    initial && initial.length
      ? initial.reduce((obj, item) => ({ ...obj, [item.id]: true }), {})
      : {}
  )
  const toggle = React.useCallback(
    (id: string) => {
      setState((prevState) => {
        if (prevState[id]) return { ...prevState, [id]: false }
        return { ...prevState, [id]: true }
      })
    },
    [setState]
  )

  const change = React.useCallback(
    (id: string, selected: boolean) => {
      setState((prevState) => {
        return { ...prevState, [id]: selected }
      })
    },
    [setState]
  )

  const clear = React.useCallback(() => {
    setState({})
  }, [setState])

  const selected = React.useMemo(() => {
    if (items) {
      return items.filter((item) => {
        return selection[item.id] || false
      })
    }

    return []
  }, [selection, items])

  return {
    selection,
    selected,
    change,
    clear,
    toggle,
  }
}

export default useSelection
