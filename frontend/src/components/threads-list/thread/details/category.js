/* jshint ignore:start */
import React from 'react';

export default function({ category, className }) {
  if (!category) return null;

  return (
    <a className={className} href={category.absolute_url}>
      {category.name}
    </a>
  );
}