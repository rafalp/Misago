import "jquery"
import "bootstrap/js/dist/util"
import "bootstrap/js/dist/dropdown"
import "bootstrap/js/dist/tooltip"
import "bootstrap/js/dist/modal"
import moment from "moment"
import htmx from "htmx.org"
import "./style/index.scss"
import initAnalytics from "./analytics"
import initColorpicker from "./colorpicker"
import initConfirmation from "./confirmation"
import initDatepicker from "./datepicker"
import initMassActions from "./massActions"
import initMassDelete from "./massDelete"
import initItemsOrdering from "./itemsOrdering"
import initTimestamps from "./timestamps"
import initTooltips from "./tooltips"
import initUserSelect from "./userSelect"
import initValidation from "./validation"
import initVersionCheck from "./versionCheck"
import { clearFieldError, hasFieldError, setFieldError } from "./fieldError"

window.moment = moment
window.htmx = htmx

window.misago = {
  initAnalytics,
  initColorpicker,
  initConfirmation,
  initDatepicker,
  initMassActions,
  initMassDelete,
  initItemsOrdering,
  initUserSelect,
  initVersionCheck,

  clearFieldError,
  hasFieldError,
  setFieldError,

  init: () => {
    const locale = document.querySelector("html").lang
    moment.locale(locale.replace("_", "-").toLowerCase())

    initTooltips()
    initTimestamps()
    initValidation()
  }
}
