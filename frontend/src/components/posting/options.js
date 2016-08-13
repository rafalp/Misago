// jshint ignore:start
import React from 'react';

export default function(props) {
  if (props.showOptions) {
    return (
      <div className="col-md-2 posting-options">
        <PinOptions
          disabled={props.disabled}
          onPinGlobally={props.onPinGlobally}
          onPinLocally={props.onPinLocally}
          onUnpin={props.onUnpin}
          pin={props.pin}
          show={props.options.pin}
        />
        <HideOptions
          disabled={props.disabled}
          hide={props.hide}
          onHide={props.onHide}
          onUnhide={props.onUnhide}
          show={props.options.hide}
        />
        <CloseOptions
          close={props.close}
          disabled={props.disabled}
          onClose={props.onClose}
          onOpen={props.onOpen}
          show={props.options.close}
        />
      </div>
    );
  } else {
    return null;
  }
}

export function CloseOptions(props) {
  if (props.show) {
    return (
      <button
        className="btn btn-default"
        disabled={props.disabled}
        onClick={props.close ? props.onOpen : props.onClose}
        title={props.close ? gettext('Closed') : gettext('Open')}
        type="button"
      >
        <span className="material-icon">
          {props.close ? 'lock' : 'lock_outline'}
        </span>
      </button>
    );
  } else {
    return null;
  }
}

export function HideOptions(props) {
  if (props.show) {
    return (
      <button
        className="btn btn-default"
        disabled={props.disabled}
        onClick={props.hide ? props.onUnhide : props.onHide}
        title={props.hide ? gettext('Hidden') : gettext('Not hidden')}
        type="button"
      >
        <span className="material-icon">
          {props.hide ? 'visibility_off' : 'visibility'}
        </span>
      </button>
    );
  } else {
    return null;
  }
}

export function PinOptions(props) {
  if (props.show) {
    let icon = null;
    let onClick = null;
    let tooltip = null;

    switch (props.pin) {
      case 0:
        icon = 'radio_button_unchecked';
        onClick = props.onPinLocally;
        tooltip = gettext("Unpinned");
        break;

      case 1:
        icon = 'info_outline';
        onClick = props.onPinGlobally;
        tooltip = gettext("Pinned locally");
        break;

      case 2:
        icon = 'info';
        onClick = props.onUnpin;
        tooltip = gettext("Pinned globally");
        break;
    }

    return (
      <button
        className="btn btn-default"
        disabled={props.disabled}
        onClick={onClick}
        title={tooltip}
        type="button"
      >
        <span className="material-icon">
          {icon}
        </span>
      </button>
    );
  } else {
    return null;
  }
}