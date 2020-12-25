import React from "react"
import { ButtonSecondary } from "../../../UI/Button"
import { CardBody } from "../../../UI/Card"
import PageTitle from "../../../UI/PageTitle"
import { Thread } from "../Thread.types"
import ThreadHeaderStarterAvatar from "./ThreadHeaderStarterAvatar"
import ThreadHeaderTidbits from "./ThreadHeaderTidbits"

interface ThreadHeaderBodyProps {
  acl: { edit: boolean }
  editThread: () => void
  thread: Thread
}

const ThreadHeaderBody: React.FC<ThreadHeaderBodyProps> = ({
  acl,
  editThread,
  thread,
}) => (
  <CardBody className="thread-header-body">
    <ThreadHeaderStarterAvatar starter={thread.starter} />
    <div className="thread-header-content">
      <div className="row">
        <div className="col">
          <PageTitle text={thread.title} />
        </div>
        <div className="col-auto">
          {acl.edit && (
            <ButtonSecondary
              icon="fas fa-pencil-alt"
              small
              onClick={editThread}
            />
          )}
        </div>
      </div>
      <ThreadHeaderTidbits thread={thread} />
    </div>
  </CardBody>
)

export default ThreadHeaderBody
