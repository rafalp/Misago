import React from "react"
import PanelLoader from "misago/components/panel-loader"

export default function () {
  return (
    <div className="panel panel-default panel-form">
      <div className="panel-heading">
        <h3 className="panel-title">
          {pgettext("change username title", "Change username")}
        </h3>
      </div>
      <PanelLoader />
    </div>
  )
}
