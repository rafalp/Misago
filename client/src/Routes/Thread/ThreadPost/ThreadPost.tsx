import React from "react"
import { Card, CardBody, CardFooter } from "../../../UI"
import { IPost } from "../Thread.types"
import ThreadPostHeader from "./ThreadPostHeader"
import ThreadPostPostbit from "./ThreadPostPostbit"

interface IThreadPostProps {
  post: IPost
}

const ThreadPost: React.FC<IThreadPostProps> = ({ post }) => (
  <div className="thread-post">
    <div className="row">
      <div className="col-auto">
        <ThreadPostPostbit post={post} />
      </div>
      <div className="col">
        <Card className="thread-post-card">
          <ThreadPostHeader post={post} />
          <CardBody className="thread-post-body">{post.body.text}</CardBody>
          <CardFooter className="thread-post-footer">post footer</CardFooter>
        </Card>
      </div>
    </div>
  </div>
)

export default React.memo(ThreadPost)
