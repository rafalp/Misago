// jshint ignore:start
import React from 'react';
import Category from './category';

export default function({ categories }) {
  return (
    <div className="categories-list">
      {categories.map((category) => {
        return (
          <Category
            category={category}
            key={category.id}
          />
        );
      })}
    </div>
  );
}