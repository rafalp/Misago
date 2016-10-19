// jshint ignore:start
import React from 'react';
import Attachment from './attachment';

export default function(props) {
  return (
    <ul className="list-unstyled editor-attachments-list">
      {props.attachments.map((item) => {
        return (
          <Attachment item={item} key={item.id || item.key} {...props} />
        );
      })}
    </ul>
  );
};
