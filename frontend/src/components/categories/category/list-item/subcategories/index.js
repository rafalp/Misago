// jshint ignore:start
import React from 'react';
import ListItem from './list-item';

export default function({ category, isFirst }) {
  if (isFirst) return null;
  if (category.subcategories.length === 0) return null;

  return (
    <div className="row subcategories-list">
      {category.subcategories.map((category) => {
        return (
          <ListItem
            category={category}
            key={category.id}
          />
        );
      })}
    </div>
  );
}