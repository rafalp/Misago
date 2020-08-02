import React from "react"
import { ButtonSecondary, CardBody, PageTitle } from "../../../UI"
import { IThread } from "../Thread.types"
import ThreadHeaderStarterAvatar from "./ThreadHeaderStarterAvatar"
import ThreadHeaderTidbits from "./ThreadHeaderTidbits"

interface IThreadHeaderBodyProps {
  acl: { edit: boolean }
  editThread: () => void
  thread: IThread
}

const ThreadHeaderBody: React.FC<IThreadHeaderBodyProps> = ({
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
              icon="pencil-alt"
              onClick={editThread}
              iconSolid
              small
            />
          )}
        </div>
      </div>
      <ThreadHeaderTidbits thread={thread} />
    </div>
  </CardBody>
)

export default ThreadHeaderBody
