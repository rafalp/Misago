import React from "react"
import { useFormContext } from "react-hook-form"
import { useFieldContext } from "../../../../UI/Form"
import useSelection from "../../../../UI/useSelection"
import { MutationError } from "../../../../types"
import { SelectedThread } from "../../Threads.types"
import ThreadsModerationSelectedThreadsListItem from "./ThreadsModerationSelectedThreadsListItem"

interface ThreadsModerationSelectedThreadsListProps {
  errors?: Record<string, MutationError>
  threads: Array<SelectedThread>
}

const ThreadsModerationSelectedThreadsList: React.FC<ThreadsModerationSelectedThreadsListProps> = ({
  errors,
  threads,
}) => {
  const context = useFieldContext()
  const name = context ? context.name : undefined

  const { register, unregister, setValue } = useFormContext() || {}
  const { change, selection, selected } = useSelection<SelectedThread>(
    threads,
    threads
  )

  React.useEffect(() => {
    if (register && unregister) {
      register({ name: "threads" })
      return () => unregister("threads")
    }
  }, [register, unregister])

  React.useEffect(() => {
    if (name && setValue) {
      setValue("threads", selected)
    }
  }, [name, setValue, selected])

  return (
    <ul className="selected-items selected-threads">
      {threads.map((thread) => (
        <ThreadsModerationSelectedThreadsListItem
          disabled={context && context.disabled}
          error={errors && errors[thread.id]}
          id={context && `${context.id}_${context.name}`}
          key={thread.id}
          selected={selection[thread.id]}
          thread={thread}
          changeSelection={change}
        />
      ))}
    </ul>
  )
}

export default ThreadsModerationSelectedThreadsList
