import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonSecondary } from "../../../UI/Button"
import { CardFooter } from "../../../UI/Card"
import { Post } from "../Thread.types"
import { useThreadReplyContext } from "../ThreadReply"

interface ThreadPostFooterProps {
  acl: { edit: boolean; reply: boolean }
  post: Post
}

const ThreadPostFooter: React.FC<ThreadPostFooterProps> = ({ acl, post }) => {
  const context = useThreadReplyContext()

  if (!context) return null

  return (
    <CardFooter className="post-footer">
      <div className="row">
        <div className="col" />
        <div className="col-auto col-right">
          {acl.edit && (
            <ButtonSecondary
              className="btn-edit"
              text={<Trans id="post.edit">Edit</Trans>}
              icon="fas fa-edit"
              small
              onClick={() => {
                context.editReply(post)
              }}
            />
          )}
          <ButtonSecondary
            className="btn-quote"
            disabled={!acl.reply}
            text={<Trans id="post.quote">Quote</Trans>}
            icon="fas fa-quote-left"
            small
            onClick={(event) => {
              const post = event.currentTarget.closest(".post")
              const article = (post as HTMLDivElement).querySelector(
                "article"
              ) as HTMLElement
              const range = document.createRange()
              range.setStart(article, 0)
              range.setEnd(article, article.childNodes.length)
              context.quote(range)
            }}
          />
          <ButtonSecondary
            className="btn-reply"
            disabled={!acl.reply}
            text={<Trans id="post.reply">Reply</Trans>}
            icon="fas fa-reply"
            small
            onClick={() => {
              if (context.startReply()) {
                let value = context.getValue().trim() + "\n\n@"
                value += post.poster ? post.poster.name : post.posterName
                context.resetValue(value.trim() + " ")
              }
            }}
          />
        </div>
      </div>
    </CardFooter>
  )
}

export default ThreadPostFooter
