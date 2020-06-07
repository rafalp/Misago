import React from "react"
import { useFormContext } from "react-hook-form"
import { useFieldContext, useSelection } from "../../../../UI"
import { IMutationError } from "../../../../types"
import { ISelectedThread } from "../../Threads.types"
import ThreadsModerationSelectedThreadsListItem from "./ThreadsModerationSelectedThreadsListItem"

interface IThreadsModerationSelectedThreadsListProps {
  errors?: Record<string, IMutationError>
  threads: Array<ISelectedThread>
}

const ThreadsModerationSelectedThreadsList: React.FC<IThreadsModerationSelectedThreadsListProps> = ({
  errors,
  threads,
}) => {
  const context = useFieldContext()
  const name = context ? context.name : undefined

  const { register, unregister, setValue } = useFormContext() || {}
  const { change, selection, selected } = useSelection<ISelectedThread>(
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
    <ul className="list-unstyled selected-threads">
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
