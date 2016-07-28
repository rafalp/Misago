/* jshint ignore:start */
import React from 'react';

export function Breadcrumb(props) {
  return <li>
    <a href={props.node.absolute_url}>{props.node.name}</a>
  </li>;
}

export default function(props) {
  return <div className="page-breadcrumbs">
    <div className="container">
      <ol className="breadcrumb">
        {props.path.map((item) => <Breadcrumb key={item.id} node={item} />)}
      </ol>
    </div>
  </div>;
}
/* jshint ignore:end */