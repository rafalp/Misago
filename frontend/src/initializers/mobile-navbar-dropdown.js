import { createRoot } from "react-dom/client"
import misago from "misago/index"
import dropdown from "../services/mobile-navbar-dropdown"

export default function initializer() {
  let rootNode = document.getElementById("mobile-navbar-dropdown-mount")
  if (rootNode) {
    const root = createRoot(rootNode)
    dropdown.init(rootNode, root)
  }
}

misago.addInitializer({
  name: "dropdown",
  initializer: initializer,
  before: "store",
})
