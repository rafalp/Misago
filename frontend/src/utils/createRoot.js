import { createRoot } from "react-dom/client"

export default function createRootForId(elementId) {
  const rootNode = document.getElementById(elementId)
  if (rootNode) {
    return createRoot(rootNode)
  }
  return null
}