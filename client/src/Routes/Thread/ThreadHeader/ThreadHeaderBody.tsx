import React from "react"
import { ButtonSecondary, CardBody, PageTitle } from "../../../UI"
import { IThread, IThreadModeration } from "../Thread.types"
import ThreadHeaderModeration from "./ThreadHeaderModeration"
import ThreadHeaderStarterAvatar from "./ThreadHeaderStarterAvatar"
import ThreadHeaderTidbits from "./ThreadHeaderTidbits"

interface IThreadHeaderBodyProps {
  acl: { edit: boolean }
  editThread: () => void
  moderation: IThreadModeration | null
  thread: IThread
}

const ThreadHeaderBody: React.FC<IThreadHeaderBodyProps> = ({
  acl,
  editThread,
  moderation,
  thread,
}) => (
  <CardBody className="thread-header-body">
    <ThreadHeaderStarterAvatar starter={thread.starter} />
    <div className="thread-header-content">
      <div className="row align-items-center">
        <div className="col">
          <PageTitle text={thread.title} />
        </div>
        <div className="col-auto">
          {acl.edit && !moderation && (
            <ButtonSecondary
              icon="pencil-alt"
              onClick={editThread}
              iconSolid
              small
            />
          )}
          {moderation && (
            <ThreadHeaderModeration
              editThread={editThread}
              moderation={moderation}
            />
          )}
        </div>
      </div>
      <ThreadHeaderTidbits thread={thread} />
    </div>
  </CardBody>
)

export default ThreadHeaderBody
