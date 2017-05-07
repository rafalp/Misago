// jshint ignore:start
import React from 'react';

export default function({ category }) {
  if (!category.description) return null;

  return (
    <div
      className="category-description"
      dangerouslySetInnerHTML={{
        __html: category.description.html
      }}
    />
  );
}