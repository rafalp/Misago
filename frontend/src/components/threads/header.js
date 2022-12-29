import React from "react"
import { Link } from "react-router"

export default class extends React.Component {
  hasGoBackButton() {
    return !!this.props.route.category.parent
  }

  getGoBackButton() {
    if (!this.props.route.category.parent) return null

    const parent = this.props.categories[this.props.route.category.parent]

    return (
      <div className="hidden-xs col-sm-2 col-lg-1">
        <Link
          className="btn btn-default btn-icon btn-aligned btn-go-back btn-block btn-outline"
          to={parent.url.index + this.props.route.list.path}
        >
          <span className="material-icon">keyboard_arrow_left</span>
        </Link>
      </div>
    )
  }

  render() {
    let headerClassName = "col-xs-12"
    if (this.hasGoBackButton()) {
      headerClassName += " col-sm-10 col-lg-11 sm-align-row-buttons"
    }

    return (
      <div className="page-header-bg">
        <div className="page-header">
          <div className="container">
            <div className="row">
              {this.getGoBackButton()}
              <div className={headerClassName}>
                <ParentCategory
                  categories={this.props.categories}
                  category={this.props.route.category.parent}
                />
                <h1>{this.props.title}</h1>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export function ParentCategory({ categories, category }) {
  if (!category) return null

  const parent = categories[category]

  return (
    <Link className="go-back-sm visible-xs-block" to={parent.url.index}>
      <span className="material-icon">chevron_left</span>
      {parent.parent ? parent.name : gettext("Threads")}
    </Link>
  )
}
