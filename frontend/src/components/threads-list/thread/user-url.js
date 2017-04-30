/* jshint ignore:start */
import React from 'react';

export default function({ children, className, url }) {
  if (url) {
    return (
      <a className={className} href={url}>
        {children}
      </a>
    );
  }

  return (
    <span className={className}>
      {children}
    </span>
  );
}