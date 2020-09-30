import React from "react"
import {
  ModalBody,
  ThreadValidationError,
  TidbitCategory,
  TidbitReplies,
  Tidbits,
} from "../../../../UI"
import { IMutationError } from "../../../../types"
import { ISelectedThread } from "../../Threads.types"

interface IThreadsModerationErrorThreadsProps {
  errors: Record<string, IMutationError>
  threads: Array<ISelectedThread>
}

const ThreadsModerationErrorThreads: React.FC<IThreadsModerationErrorThreadsProps> = ({
  errors,
  threads,
}) => (
  <ModalBody className="modal-threads-errors">
    <ul className="threads-errors">
      {threads.map((thread) => {
        if (!errors[thread.id]) return null

        return (
          <li key={thread.id} className="threads-errors-thread">
            <ThreadValidationError error={errors[thread.id]}>
              {({ message }) => (
                <div className="threads-errors-thread-error">{message}</div>
              )}
            </ThreadValidationError>
            <div className="threads-errors-thread-title">{thread.title}</div>
            <div className="threads-errors-thread-tidbits">
              <Tidbits>
                {thread.category.parent && (
                  <TidbitCategory
                    category={thread.category.parent}
                    disabled
                    parent
                  />
                )}
                <TidbitCategory category={thread.category} disabled />
                {thread.replies > 0 && (
                  <TidbitReplies value={thread.replies} />
                )}
              </Tidbits>
            </div>
          </li>
        )
      })}
    </ul>
  </ModalBody>
)

export default ThreadsModerationErrorThreads
