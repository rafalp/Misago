import React from "react"

export default function({ value, onChange }) {
  return (
    <input
      aria-haspopup="true"
      aria-expanded="false"
      aria-controls="dropdown-menu dropdown-search-results"
      autoComplete="off"
      className="form-control"
      value={value}
      onChange={onChange}
      placeholder={gettext("Search")}
      role="combobox"
      type="text"
    />
  )
}
