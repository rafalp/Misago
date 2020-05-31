import { Plural, Trans } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
import { useBulkActionLimit } from "../../../Context"
import {
  Form,
  FormFooter,
  ModalAlert,
  ModalFormBody,
  ModalFooter,
  RootError,
  useSelectionErrors,
} from "../../../UI"
import { IThread } from "../Threads.types"
import ThreadsModerationModal from "./ThreadsModerationModal"
import { ThreadsModerationModalAction } from "./ThreadsModerationModalContext"
import ThreadsModerationSelectedThreads from "./ThreadsModerationSelectedThreads"
import useDeleteThreadsMutation from "./deleteThreads"

interface IFormValues {
  threads: Array<IThread>
}

const ThreadsModerationModalDelete: React.FC = () => {
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

  return (
    <ThreadsModerationModal
      action={ThreadsModerationModalAction.DELETE}
      title={<Trans id="moderation.delete_threads">Delete threads</Trans>}
    >
      {({ close, threads }) => {
        return (
          <Form<IFormValues>
            id="delete_threads_form"
            disabled={loading}
            defaultValues={{ threads }}
            validationSchema={DeleteThreadsSchema}
            onSubmit={async ({ clearError, setError, data: { threads } }) => {
              clearError()
              clearThreadsErrors()

              const result = await deleteThreads(threads)
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
      }}
    </ThreadsModerationModal>
  )
}

export default ThreadsModerationModalDelete
