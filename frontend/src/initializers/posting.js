import { createRoot } from "react-dom/client"
import misago from "misago/index"
import ajax from "../services/ajax"
import posting from "../services/posting"
import snackbar from "../services/snackbar"

export default function initializer() {
  const rootNode = document.getElementById("posting-mount")
  const root = createRoot(rootNode)
  posting.init(ajax, snackbar, rootNode, root)
}

misago.addInitializer({
  name: "posting",
  initializer: initializer,
})
