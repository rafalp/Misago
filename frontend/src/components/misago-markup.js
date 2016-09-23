// jshint ignore:start
import React from 'react';

export default function(props) {
 return (
    <article className="misago-markup" dangerouslySetInnerHTML={{__html: props.markup}} />
  );
}
