import React from "react"
import Field from "./field"

export default function ({ fields, name }) {
  return (
    <div className="panel panel-default panel-profile-details-group">
      <div className="panel-heading">
        <h3 className="panel-title">{name}</h3>
      </div>
      <div className="panel-body">
        <div className="form-horizontal">
          {fields.map(({ fieldname, html, name, text, url }) => {
            return (
              <Field
                key={fieldname}
                name={name}
                html={html}
                text={text}
                url={url}
              />
            )
          })}
        </div>
      </div>
    </div>
  )
}
