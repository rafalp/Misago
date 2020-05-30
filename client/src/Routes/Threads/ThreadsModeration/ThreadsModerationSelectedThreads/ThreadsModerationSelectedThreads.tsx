import { Trans } from "@lingui/macro"
import React from "react"
import { Field, FieldError, ValidationError } from "../../../../UI"
import { IMutationError } from "../../../../types"
import { ISelectedThread } from "./ThreadsModerationSelectedThreads.types"
import ThreadsModerationSelectedThreadsButton from "./ThreadsModerationSelectedThreadsButton"
import ThreadsModerationSelectedThreadsList from "./ThreadsModerationSelectedThreadsList"

interface IThreadsModerationSelectedThreadsProps {
  errors?: Record<string, IMutationError>
  threads: Array<ISelectedThread>
}

const ThreadsModerationSelectedThreads: React.FC<IThreadsModerationSelectedThreadsProps> = ({
  errors,
  threads,
}) => {
  const [isOpen, setState] = React.useState<boolean>(threads.length < 3)

  return (
    <Field
      label={<Trans id="moderation.selected_threads">Selected threads</Trans>}
      name="threads"
      input={
        <>
          <div className={isOpen ? "" : "d-none"}>
            <ThreadsModerationSelectedThreadsList
              errors={errors}
              threads={threads}
            />
          </div>
          {!isOpen && (
            <ThreadsModerationSelectedThreadsButton
              threadsCount={threads.length}
              onClick={() => setState(true)}
            />
          )}
        </>
      }
      error={(error, value) => (
        <ValidationError error={error} value={value}>
          {({ message }) => <FieldError>{message}</FieldError>}
        </ValidationError>
      )}
    />
  )
}

export default ThreadsModerationSelectedThreads
