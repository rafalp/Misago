// jshint ignore:start
import React from 'react';

export default function(props) {
  return <select id={props.id || null}
                 className={props.className || 'form-control'}
                 value={props.value}
                 onChange={props.onChange}>
    {props.choices.map((item) => {
      return <option disabled={item.disabled || false}
                     value={item.value}
                     key={item.value}>
        {'- - '.repeat(item.level) + item.label}
      </option>
    })}
  </select>;
}