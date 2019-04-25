import "jquery"
import "bootstrap/js/dist/util"
import "bootstrap/js/dist/dropdown"
import "bootstrap/js/dist/tooltip"
import "bootstrap/js/dist/modal"
import "./style/index.scss"
import initConfirmation from "./confirmation"
import initMassActions from "./massActions"
import initMassDelete from "./massDelete"
import initTimestamps from "./timestamps"
import initTooltips from "./tooltips"
import initValidation from "./validation"

initTooltips()
initTimestamps()
initValidation()

window.misago = {
  initConfirmation,
  initMassActions,
  initMassDelete
}
