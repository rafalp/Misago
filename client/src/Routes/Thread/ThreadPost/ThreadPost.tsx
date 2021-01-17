import React from "react"
import { Card, CardBody } from "../../../UI/Card"
import RichText from "../../../UI/RichText"
import { Post } from "../Thread.types"
import ThreadPostFooter from "./ThreadPostFooter"
import ThreadPostHeader from "./ThreadPostHeader"
import ThreadPostPostbit from "./ThreadPostPostbit"
import usePostAcl from "./usePostAcl"
import useScrollPostIntoView from "./useScrollPostIntoView"

interface ThreadPostProps {
  post: Post
  threadId: string
  threadSlug: string
  page?: number
  isClosed?: boolean
  isSelected?: boolean
  toggleSelection?: ((id: string) => void) | null
}

const ThreadPost: React.FC<ThreadPostProps> = ({
  post,
  threadId,
  threadSlug,
  page,
  isClosed,
  isSelected,
  toggleSelection,
}) => {
  const scrollIntoView = useScrollPostIntoView()
  const acl = usePostAcl(post, isClosed)

  return (
    <div className="post" id={"post-" + post.id} ref={scrollIntoView}>
      <div className="row">
        <div className="col-auto post-sidebit">
          <ThreadPostPostbit post={post} />
        </div>
        <div className="col">
          <Card className="post-card">
            <ThreadPostHeader
              acl={acl}
              post={post}
              threadId={threadId}
              threadSlug={threadSlug}
              page={page}
              isSelected={isSelected}
              toggleSelection={toggleSelection}
            />
            <CardBody className="post-body">
              <RichText
                author={post.poster ? post.poster.name : post.posterName}
                postId={post.id}
                richText={post.richText}
              />
            </CardBody>
            <ThreadPostFooter acl={acl} post={post} />
          </Card>
        </div>
      </div>
    </div>
  )
}

export default React.memo(ThreadPost)
