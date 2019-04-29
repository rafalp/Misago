import "jquery"
import "bootstrap/js/dist/util"
import "bootstrap/js/dist/dropdown"
import "bootstrap/js/dist/tooltip"
import "bootstrap/js/dist/modal"
import moment from "moment"
import "./style/index.scss"
import initConfirmation from "./confirmation"
import initDatepicker from "./datepicker"
import initMassActions from "./massActions"
import initMassDelete from "./massDelete"
import initTimestamps from "./timestamps"
import initTooltips from "./tooltips"
import initValidation from "./validation"

moment.locale(document.querySelector("html").lang)

initTooltips()
initTimestamps()
initValidation()

window.misago = {
  initConfirmation,
  initDatepicker,
  initMassActions,
  initMassDelete
}
