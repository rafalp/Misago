export class PageTitle {
  init(forumName) {
    this._forumName = forumName;
  }

  set(title) {
    if (typeof title === 'string') {
      title = {title: title};
    }

    let finalTitle = title.title;

    if (title.page) {
      let pageLabel = interpolate(gettext('page: %(page)s'), {
        page: title.page
      }, true);

      finalTitle += ' (' + pageLabel + ')';
    }

    if (title.parent) {
      finalTitle += ' | ' + title.parent;
    }

    document.title = finalTitle + ' | ' + this._forumName;
  }
}

export default new PageTitle();
