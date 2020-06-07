import { Plural } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
import { useBulkActionLimit } from "../../../../Context"
import {
  Form,
  FormFooter,
  ModalAlert,
  ModalFormBody,
  ModalFooter,
  RootError,
  useSelectionErrors,
} from "../../../../UI"
import { ICategory } from "../../../../types"
import { IThread } from "../../Threads.types"
import ThreadsModerationModalError from "../ThreadsModerationModalError"
import ThreadsModerationSelectedThreads from "../ThreadsModerationSelectedThreads"
import useDeleteThreadsMutation from "../deleteThreads"

interface IThreadsModerationModalDeleteFormProps {
  category?: ICategory | null
  threads: Array<IThread>
  close: () => void
}

interface IFormValues {
  threads: Array<IThread>
}

const ThreadsModerationModalDeleteForm: React.FC<IThreadsModerationModalDeleteFormProps> = ({
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
  const DeleteThreadsSchema = Yup.object().shape({
    threads: Yup.array()
      .min(1, "value_error.list.min_items")
      .max(bulkActionLimit, "value_error.list.max_items"),
  })

  if (data?.deleteThreads.errors) {
    return (
      <ThreadsModerationModalError
        errors={data.deleteThreads.errors}
        threads={threads}
        close={close}
      />
    )
  }

  return (
    <Form<IFormValues>
      id="delete_threads_form"
      disabled={loading}
      defaultValues={{ threads }}
      validationSchema={DeleteThreadsSchema}
      onSubmit={async ({ clearError, setError, data: { threads } }) => {
        clearError()
        clearThreadsErrors()

        try {
          const result = await deleteThreads(threads, category)
          const { errors } = result.data?.deleteThreads || {}

          if (errors) {
            setThreadsErrors(threads, errors)
            errors?.forEach(({ location, type, message }) => {
              const field = location.join(".")
              setError(field, type, message)
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

export default ThreadsModerationModalDeleteForm
