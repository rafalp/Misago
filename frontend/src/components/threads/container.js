import React from "react"
import PageLead from "misago/components/page-lead"
import PageContainer from "../PageContainer"
import ThreadsToolbar from "./ThreadsToolbar"

export default class extends React.Component {
  getCategoryDescription() {
    if (this.props.pageLead) {
      return (
        <div className="category-description">
          <div className="page-lead lead">
            <p>{this.props.pageLead}</p>
          </div>
        </div>
      )
    } else if (this.props.route.category.description) {
      return (
        <div className="category-description">
          <PageLead copy={this.props.route.category.description.html} />
        </div>
      )
    } else {
      return null
    }
  }

  getDisableToolbar() {
    return (
      !this.props.isLoaded || this.props.isBusy || this.props.busyThreads.length
    )
  }

  render() {
    const { root } = this.props
    const { category, categories, categoriesMap } = this.props.route
    const topCategory = getTopCategory(root, category, categoriesMap)

    return (
      <PageContainer>
        {this.getCategoryDescription()}
        <ThreadsToolbar
          api={this.props.api}
          baseUrl={category.url.index}
          category={category}
          categories={categories}
          categoriesMap={categoriesMap}
          topCategory={topCategory}
          topCategories={categories.filter((cat) => cat.parent === root.id)}
          subCategories={
            !!topCategory
              ? categories.filter((cat) => cat.parent === topCategory.id)
              : []
          }
          subCategory={category.level === 2 ? category : null}
          subcategories={this.props.subcategories}
          list={this.props.route.list}
          lists={this.props.route.lists}
          threads={this.props.threads}
          addThreads={this.props.addThreads}
          startThread={this.props.startThread}
          freezeThread={this.props.freezeThread}
          deleteThread={this.props.deleteThread}
          updateThread={this.props.updateThread}
          selection={this.props.selection}
          moderation={this.props.moderation}
          route={this.props.route}
          user={this.props.user}
          disabled={
            !this.props.isLoaded ||
            this.props.isBusy ||
            this.props.busyThreads.length
          }
        />
        {this.props.children}
      </PageContainer>
    )
  }
}

const getTopCategory = (root, category, categoriesMap) => {
  if (!category.parent) return null
  if (category.parent === root.id) return category
  return categoriesMap[category.parent]
}
