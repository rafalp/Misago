import React from "react"
import { Card, CardBody, CardFooter } from "../../../UI"
import { IPost } from "../Thread.types"
import ThreadPostEditForm from "./ThreadPostEditForm"
import ThreadPostHeader from "./ThreadPostHeader"
import ThreadPostPostbit from "./ThreadPostPostbit"
import usePostAcl from "./usePostAcl"

interface IThreadPostProps {
  post: IPost
  threadId: string
  page?: number
  isClosed?: boolean
  isEdited?: boolean
  isSelected?: boolean
  toggleSelection?: ((id: string) => void) | null
}

const ThreadPost: React.FC<IThreadPostProps> = ({
  post,
  threadId,
  page,
  isClosed,
  isEdited,
  isSelected,
  toggleSelection,
}) => {
  const acl = usePostAcl(post, isClosed)
  const [edit, setEdit] = React.useState(isEdited || false)
  const editPost = () => setEdit(true)

  return (
    <div className="post">
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
              page={page}
              isSelected={isSelected}
              editPost={editPost}
              toggleSelection={toggleSelection}
            />
            {edit ? (
              <ThreadPostEditForm post={post} close={() => setEdit(false)} />
            ) : (
              <>
                <CardBody className="post-body">{post.body.text}</CardBody>
                <CardFooter className="post-footer">post footer</CardFooter>
              </>
            )}
          </Card>
        </div>
      </div>
    </div>
  )
}

export default React.memo(ThreadPost)
