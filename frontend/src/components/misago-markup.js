// jshint ignore:start
import React from 'react';
import onebox from 'misago/services/one-box';


export default function(props) {
  return (
    <article
      className="misago-markup"
      dangerouslySetInnerHTML={{__html: props.markup}}
      ref={node => onebox.render(node)}
    />
  );
}
