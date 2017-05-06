/* jshint ignore:start */
import React from 'react';

export default function({ children, className, title, url }) {
  if (url) {
    return (
      <a
        className={className}
        href={url}
        title={title}
      >
        {children}
      </a>
    );
  }

  return (
    <span
      className={className}
      title={title}
    >
      {children}
    </span>
  );
}