import React from "react"
import ReactDom from "react-dom"

const portal = (children: React.ReactNode): React.ReactPortal | null => {
  const root = document.getElementById("portals-root")
  if (!root) return null
  return ReactDom.createPortal(children, root)
}

export default portal
