export class PageTitle {
  init(indexTitle, forumName) {
    this._indexTitle = indexTitle
    this._forumName = forumName
  }

  set(title) {
    if (!title) {
      document.title = this._indexTitle || this._forumName
      return
    }

    if (typeof title === "string") {
      title = { title: title }
    }

    let finalTitle = title.title

    if (title.page > 1) {
      const pageLabel = interpolate(
        pgettext("page title pagination", "page: %(page)s"),
        {
          page: title.page,
        },
        true
      )

      finalTitle += " (" + pageLabel + ")"
    }

    if (title.parent) {
      finalTitle += " | " + title.parent
    }

    document.title = finalTitle + " | " + this._forumName
  }
}

export default new PageTitle()
