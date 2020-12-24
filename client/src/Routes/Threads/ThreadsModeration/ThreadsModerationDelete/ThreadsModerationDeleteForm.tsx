import { Plural } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
import { useBulkActionLimit } from "../../../../Context"
import { Form, FormFooter } from "../../../../UI/Form"
import { ModalAlert, ModalFormBody, ModalFooter } from "../../../../UI/Modal"
import RootError from "../../../../UI/RootError"
import { useSelectionErrors } from "../../../../UI/useSelectionErrors"
import { ICategory } from "../../../../types"
import { IThread } from "../../Threads.types"
import ThreadsModerationError from "../ThreadsModerationError"
import ThreadsModerationSelectedThreads from "../ThreadsModerationSelectedThreads"
import useDeleteThreadsMutation from "./useDeleteThreadsMutation"

interface ThreadsModerationDeleteFormProps {
  category?: ICategory | null
  threads: Array<IThread>
  close: () => void
}

interface FormValues {
  threads: Array<IThread>
}

const ThreadsModerationDeleteForm: React.FC<ThreadsModerationDeleteFormProps> = ({
  category,
  threads,
  close,
}) => {
  const {
    errors: threadsErrors,
    clearErrors: clearThreadsErrors,
    setErrors: setThreadsErrors,
  } = useSelectionErrors<IThread>("threads")

  const {
    data,
    loading,
    deleteThreads,
    error: graphqlError,
  } = useDeleteThreadsMutation()

  const bulkActionLimit = useBulkActionLimit()
  const validators = Yup.object().shape({
    threads: Yup.array()
      .min(1, "value_error.list.min_items")
      .max(bulkActionLimit, "value_error.list.max_items"),
  })

  if (data?.deleteThreads.errors) {
    return (
      <ThreadsModerationError
        errors={data.deleteThreads.errors}
        threads={threads}
        close={close}
        forDelete
      />
    )
  }

  return (
    <Form<FormValues>
      id="delete_threads_form"
      disabled={loading}
      defaultValues={{ threads }}
      validators={validators}
      onSubmit={async ({ clearErrors, setError, data: { threads } }) => {
        clearErrors()
        clearThreadsErrors()

        try {
          const result = await deleteThreads(threads, category)
          const { errors } = result.data?.deleteThreads || {}

          if (errors) {
            setThreadsErrors(threads, errors)
            errors?.forEach(({ location, type, message }) => {
              const field = location.join(".")
              setError(field, { type, message })
            })
          } else {
            close()
          }
        } catch (error) {
          // do nothing when deleteThreads throws
          return
        }
      }}
    >
      <RootError
        graphqlError={graphqlError}
        dataErrors={data?.deleteThreads.errors}
      >
        {({ message }) => <ModalAlert>{message}</ModalAlert>}
      </RootError>
      <ModalFormBody>
        <ThreadsModerationSelectedThreads
          errors={threadsErrors}
          max={bulkActionLimit}
          min={1}
          threads={threads}
        />
      </ModalFormBody>
      <ModalFooter>
        <FormFooter
          submitText={
            <Plural
              id="moderation.delete_threads.submit"
              value={threads.length}
              one="Delete # thread"
              other="Delete # threads"
            />
          }
          loading={loading}
          danger
          onCancel={close}
        />
      </ModalFooter>
    </Form>
  )
}

export default ThreadsModerationDeleteForm
