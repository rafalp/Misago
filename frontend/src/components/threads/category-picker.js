import React from "react"
import { Link } from "react-router"

export class Subcategory extends React.Component {
  getUrl() {
    if (this.props.listPath) {
      return this.props.category.url.index + this.props.listPath
    } else {
      return this.props.category.url.index
    }
  }

  render() {
    return (
      <li>
        <Link to={this.getUrl()} className="btn btn-link">
          {this.props.category.name}
        </Link>
      </li>
    )
  }
}

export default class extends React.Component {
  render() {
    return (
      <div className="dropdown category-picker">
        <button
          type="button"
          className="btn btn-default btn-outline dropdown-toggle btn-block"
          data-toggle="dropdown"
          aria-haspopup="true"
          aria-expanded="false"
        >
          <span className="material-icon">label_outline</span>
          <span className="hidden-xs">{gettext("Category")}</span>
        </button>
        <ul className="dropdown-menu stick-to-bottom categories-menu">
          {this.props.choices.map(id => {
            if (this.props.categories[id]) {
              return (
                <Subcategory
                  category={this.props.categories[id]}
                  listPath={this.props.list.path}
                  key={id}
                />
              )
            } else {
              return null
            }
          })}
        </ul>
      </div>
    )
  }
}
