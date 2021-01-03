import { Trans } from "@lingui/macro"
import React from "react"
import { Link } from "react-router-dom"
import Icon from "../../UI/Icon"
import { RichTextQuoteAuthor } from "../../types"
import * as urls from "../../urls"

interface RichTextQuoteHeaderProps {
  author: RichTextQuoteAuthor
  post: number | null
}

const RichTextQuoteHeader: React.FC<RichTextQuoteHeaderProps> = ({
  author,
  post,
}) => (
  <div className="rich-text-quote-header" data-noquote="1">
    <div className="rich-text-quote-title">
      <Trans id="rich_text.quote">
        {author.id && author.slug ? (
          <Link to={urls.user({ id: author.id, slug: author.slug })}>
            {author.name}
          </Link>
        ) : (
          <span>{author.name}</span>
        )}{" "}
        said:
      </Trans>
    </div>
    {post && (
      <Link className="btn btn-secondary btn-sm" to={urls.post({ id: post })}>
        <Icon icon="fas fa-reply" fixedWidth />
      </Link>
    )}
  </div>
)

export default RichTextQuoteHeader
