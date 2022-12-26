import React from "react"
import { Link } from "react-router"

const ThreadsCategoryPicker = ({ allItems, parentUrl, category, categories, list }) => (
  <div className="dropdown threads-category-picker">
    <button
      type="button"
      className="btn btn-default btn-outline dropdown-toggle btn-block"
      data-toggle="dropdown"
      aria-haspopup="true"
      aria-expanded="false"
    >
      {category && (
        <span className="material-icon" style={{ color: category.color || "inherit"}}>
          label
        </span>
      )}
      {category && category.short_name && (
        <span className={category.short_name && "hidden-md hidden-lg"}>
          {category.short_name}
        </span>
      )}
      {category ? (
        <span className={category.short_name && "hidden-xs hidden-sm"}>
          {category.name}
        </span>
      ): allItems}
    </button>
    <ul className="dropdown-menu stick-to-bottom">
      <li>
        <Link to={parentUrl + list.path}>
          {allItems}
        </Link>
      </li>
      <li role="separator" className="divider" />
      {categories.map((choice) => (
        <li key={choice.id}>
          <Link to={choice.url.index + list.path}>
            <span className="material-icon" style={{ color: choice.color || "inherit"}}>
              label
            </span>
            {choice.name}
          </Link>
        </li>
      ))}
    </ul>
  </div>
)

export default ThreadsCategoryPicker