import React from "react"

export default function (props) {
  if (!props.showOptions) return null

  const { columns } = props

  let className = "col-xs-12 xs-margin-top"

  if (columns === 1) {
    className += " col-sm-2"
  } else {
    className += " sm-margin-top"
  }

  if (columns === 3) {
    className += " col-md-3"
  } else {
    className += " col-md-2"
  }
  className += " posting-options"

  const columnClassName = "col-xs-" + 12 / columns

  let textClassName = "btn-text"
  if (columns === 3) {
    textClassName += " visible-sm-inline-block"
  } else if (columns === 2) {
    textClassName += " hidden-md hidden-lg"
  } else {
    textClassName += " hidden-sm"
  }

  return (
    <div className={className}>
      <div className="row">
        <PinOptions
          className={columnClassName}
          disabled={props.disabled}
          onPinGlobally={props.onPinGlobally}
          onPinLocally={props.onPinLocally}
          onUnpin={props.onUnpin}
          pin={props.pin}
          show={props.options.pin}
          textClassName={textClassName}
        />
        <HideOptions
          className={columnClassName}
          disabled={props.disabled}
          hide={props.hide}
          onHide={props.onHide}
          onUnhide={props.onUnhide}
          show={props.options.hide}
          textClassName={textClassName}
        />
        <CloseOptions
          className={columnClassName}
          close={props.close}
          disabled={props.disabled}
          onClose={props.onClose}
          onOpen={props.onOpen}
          show={props.options.close}
          textClassName={textClassName}
        />
      </div>
    </div>
  )
}

export function CloseOptions(props) {
  if (!props.show) return null

  const label = props.close
    ? pgettext("posting form", "Closed")
    : pgettext("posting form", "Open")

  return (
    <div className={props.className}>
      <button
        className="btn btn-default btn-block"
        disabled={props.disabled}
        onClick={props.close ? props.onOpen : props.onClose}
        title={label}
        type="button"
      >
        <span className="material-icon">
          {props.close ? "lock" : "lock_outline"}
        </span>
        <span className={props.textClassName}>{label}</span>
      </button>
    </div>
  )
}

export function HideOptions(props) {
  if (!props.show) return null

  const label = props.hide
    ? pgettext("posting form", "Hidden")
    : pgettext("posting form", "Not hidden")

  return (
    <div className={props.className}>
      <button
        className="btn btn-default btn-block"
        disabled={props.disabled}
        onClick={props.hide ? props.onUnhide : props.onHide}
        title={label}
        type="button"
      >
        <span className="material-icon">
          {props.hide ? "visibility_off" : "visibility"}
        </span>
        <span className={props.textClassName}>{label}</span>
      </button>
    </div>
  )
}

export function PinOptions(props) {
  if (!props.show) return null

  let icon = null
  let onClick = null
  let label = null

  switch (props.pin) {
    case 0:
      icon = "radio_button_unchecked"
      onClick = props.onPinLocally
      label = pgettext("posting form", "Unpinned")
      break

    case 1:
      icon = "bookmark_outline"
      onClick = props.onPinGlobally
      label = pgettext("posting form", "Pinned in category")

      if (props.show == 2) {
        onClick = props.onPinGlobally
      } else {
        onClick = props.onUnpin
      }

      break

    case 2:
      icon = "bookmark"
      onClick = props.onUnpin
      label = pgettext("posting form", "Pinned globally")
      break
  }

  return (
    <div className={props.className}>
      <button
        className="btn btn-default btn-block"
        disabled={props.disabled}
        onClick={onClick}
        title={label}
        type="button"
      >
        <span className="material-icon">{icon}</span>
        <span className={props.textClassName}>{label}</span>
      </button>
    </div>
  )
}
