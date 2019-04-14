import $ from "jquery"

const initTooltips = () => {
  $('[data-tooltip="top"]').tooltip({ placement: "top" })
  $('[data-tooltip="bottom"]').tooltip({ placement: "bottom" })
}

export default initTooltips
