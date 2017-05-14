// jshint ignore:start
import React from 'react';

export default function(props) {
  return (
    <div className="categories-list">
      <ul className="list-group">
        <li className="list-group-item empty-message">
          <p className="lead">
            {gettext("No categories exist or you don't have permission to see them.")}
          </p>
        </li>
      </ul>
    </div>
  );
}