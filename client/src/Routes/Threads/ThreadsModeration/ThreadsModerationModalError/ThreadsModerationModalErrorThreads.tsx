import React from "react"
import { ModalBody, ThreadValidationError } from "../../../../UI"
import { IMutationError } from "../../../../types"
import { ISelectedThread } from "../../Threads.types"

interface IThreadsModerationModalErrorThreadsProps {
  errors: Record<string, IMutationError>
  threads: Array<ISelectedThread>
}

const ThreadsModerationModalErrorThreads: React.FC<IThreadsModerationModalErrorThreadsProps> = ({
  errors,
  threads,
}) => (
  <ModalBody>
    <ul className="list-unstyled threads-errors">
      {threads.map((thread) => {
        if (!errors[thread.id]) return null

        return (
          <li key={thread.id} className="threads-errors-thread">
            <div className="threads-errors-thread-title">{thread.title}</div>
            <ThreadValidationError error={errors[thread.id]}>
              {({ message }) => (
                <div className="threads-errors-thread-error">{message}</div>
              )}
            </ThreadValidationError>
          </li>
        )
      })}
    </ul>
  </ModalBody>
)

export default ThreadsModerationModalErrorThreads
