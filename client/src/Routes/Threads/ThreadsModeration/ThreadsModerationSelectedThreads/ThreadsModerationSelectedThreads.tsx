import { Trans } from "@lingui/macro"
import React from "react"
import { Field, FieldError } from "../../../../UI/Form"
import { ThreadsValidationError } from "../../../../UI/ValidationError"
import { IMutationError } from "../../../../types"
import { ISelectedThread } from "../../Threads.types"
import ThreadsModerationSelectedThreadsButton from "./ThreadsModerationSelectedThreadsButton"
import ThreadsModerationSelectedThreadsList from "./ThreadsModerationSelectedThreadsList"

interface IThreadsModerationSelectedThreadsProps {
  errors?: Record<string, IMutationError>
  threads: Array<ISelectedThread>
  min: number
  max: number
}

const ThreadsModerationSelectedThreads: React.FC<IThreadsModerationSelectedThreadsProps> = ({
  errors,
  threads,
  min,
  max,
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
        <ThreadsValidationError
          error={error}
          max={max}
          min={min}
          value={value.length}
        >
          {({ message }) => <FieldError>{message}</FieldError>}
        </ThreadsValidationError>
      )}
    />
  )
}

export default ThreadsModerationSelectedThreads
