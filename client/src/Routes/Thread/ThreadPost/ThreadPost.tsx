import React from "react"
import { Card, CardBody, CardFooter } from "../../../UI/Card"
import RichText from "../../../UI/RichText"
import { IPost } from "../Thread.types"
import ThreadPostHeader from "./ThreadPostHeader"
import ThreadPostPostbit from "./ThreadPostPostbit"
import usePostAcl from "./usePostAcl"
import useScrollPostIntoView from "./useScrollPostIntoView"

interface ThreadPostProps {
  post: IPost
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
              <RichText richText={post.richText} />
            </CardBody>
            <CardFooter className="post-footer">post footer</CardFooter>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default React.memo(ThreadPost)
