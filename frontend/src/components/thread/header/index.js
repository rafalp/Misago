/* jshint ignore:start */
import React from 'react';
import Breadcrumbs from './breadcrumbs';
import Stats from './stats';

export default function(props) {
  return <div className="page-header with-stats with-breadcrumbs">
    <Breadcrumbs path={props.thread.path} />
    <div className="container">
      <h1>{props.thread.title}</h1>
    </div>
    <Stats thread={props.thread} />
  </div>;
}