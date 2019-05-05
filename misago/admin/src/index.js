import "jquery"
import "bootstrap/js/dist/util"
import "bootstrap/js/dist/dropdown"
import "bootstrap/js/dist/tooltip"
import "bootstrap/js/dist/modal"
import moment from "moment"
import "./style/index.scss"
import initAnalytics from "./analytics"
import initConfirmation from "./confirmation"
import initDatepicker from "./datepicker"
import initMassActions from "./massActions"
import initMassDelete from "./massDelete"
import initTimestamps from "./timestamps"
import initTooltips from "./tooltips"
import initValidation from "./validation"

window.moment = moment
window.misago = {
  initAnalytics,
  initConfirmation,
  initDatepicker,
  initMassActions,
  initMassDelete,

  init: () => {
    const locale = document.querySelector("html").lang
    moment.locale(locale.replace("_", "-").toLowerCase())

    initTooltips()
    initTimestamps()
    initValidation()
  }
}
