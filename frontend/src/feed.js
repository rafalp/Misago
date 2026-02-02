import * as snackbar from "./snackbars"
import quote from "./Quote"

class Feed {
  activate = () => {
    document.addEventListener("click", this.onClick)
  }

  onClick = (event) => {
    const target = event.target.closest("[mg-feed-action]")
    const action = target ? target.getAttribute("mg-feed-action") : null

    if (!action) {
      return null
    }

    const post = target.closest("[mg-feed-item]")

    event.preventDefault()

    if (!post) {
      return null
    }

    if (action === "quote") {
      this.quotePost(post)
    }
  }

  quotePost = (post) => {
    const range = document.createRange()
    range.selectNodeContents(post.querySelector("[misago-quote-root]"))

    const quoteMarkup = quote.getSelectionQuote(quote.getRangeRoot(range))
    const form = document.getElementById("misago-htmx-quick-reply")

    quote.updateForm(form, quoteMarkup)
  }
}

export default Feed
