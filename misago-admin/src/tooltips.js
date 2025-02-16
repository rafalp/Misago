import $ from "jquery"

const initTooltips = () => {
  $('[data-tooltip="top"]').tooltip({ placement: "top" })
  $('[data-tooltip="bottom"]').tooltip({ placement: "bottom" })
  $('[data-tooltip="left"]').tooltip({ placement: "left" })
}

export default initTooltips
