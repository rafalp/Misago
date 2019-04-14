import "jquery"
import "bootstrap/js/dist/util"
import "bootstrap/js/dist/dropdown"
import "bootstrap/js/dist/tooltip"
import "bootstrap/js/dist/modal"
import "./style/index.scss"
import initMassActions from "./actions"
import initTimestamps from "./timestamps"
import initTooltips from "./tooltips"

initTooltips()
initTimestamps()

window.misago = {
  initMassActions
}
