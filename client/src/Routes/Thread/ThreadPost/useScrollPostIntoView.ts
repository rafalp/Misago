import React from "react"

const useScrollPostIntoView = () => {
  return React.useCallback((element: HTMLDivElement | null) => {
    if (element !== null && window.location.hash === "#" + element.id) {
      element.scrollIntoView()
    }
  }, [])
}

export default useScrollPostIntoView
