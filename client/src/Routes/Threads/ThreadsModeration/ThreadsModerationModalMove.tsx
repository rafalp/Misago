import { Plural, Trans } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
import {
  CategorySelect,
  Field,
  FieldError,
  Form,
  FormFooter,
  ModalAlert,
  ModalFormBody,
  ModalFooter,
  RootError,
  CategoryValidationError,
  useSelectionErrors,
} from "../../../UI"
import { IThread } from "../Threads.types"
import ThreadsModerationModal from "./ThreadsModerationModal"
import { ThreadsModerationModalAction } from "./ThreadsModerationModalContext"
import ThreadsModerationSelectedThreads from "./ThreadsModerationSelectedThreads"
import useMoveThreadsMutation from "./moveThreads"

interface IFormValues {
  category: string
  threads: Array<IThread>
}

const ThreadsModerationModalMove: React.FC = () => {
  const {
    errors: threadsErrors,
    clearErrors: clearThreadsErrors,
    setErrors: setThreadsErrors,
  } = useSelectionErrors<IThread>("threads")

  const {
    data,
    loading,
    moveThreads,
    error: graphqlError,
  } = useMoveThreadsMutation()

  const MoveThreadsSchema = Yup.object().shape({
    category: Yup.string().required("value_error.missing"),
    threads: Yup.array()
      .required("value_error.missing")
      .min(1, "value_error.missing"),
  })

  return (
    <ThreadsModerationModal
      action={ThreadsModerationModalAction.MOVE}
      title={<Trans id="moderation.move_threads">Move threads</Trans>}
    >
      {({ close, threads }) => {
        return (
          <Form<IFormValues>
            id="move_threads_form"
            disabled={loading}
            defaultValues={{ threads, category: "" }}
            validationSchema={MoveThreadsSchema}
            onSubmit={async ({
              clearError,
              setError,
              data: { category, threads },
            }) => {
              clearError()
              clearThreadsErrors()

              const data = await moveThreads(threads, category)
              const { errors } = data.data?.moveThreads || {}
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
              dataErrors={data?.moveThreads.errors}
            >
              {({ message }) => <ModalAlert>{message}</ModalAlert>}
            </RootError>
            <ModalFormBody>
              <ThreadsModerationSelectedThreads
                errors={threadsErrors}
                threads={threads}
              />
              <Field
                label={
                  <Trans id="moderation.new_category">New category</Trans>
                }
                name="category"
                input={<CategorySelect />}
                error={(error, value) => (
                  <CategoryValidationError error={error} value={value}>
                    {({ message }) => <FieldError>{message}</FieldError>}
                  </CategoryValidationError>
                )}
              />
            </ModalFormBody>
            <ModalFooter>
              <FormFooter
                submitText={
                  <Plural
                    id="moderation.move_threads.submit"
                    value={threads.length}
                    one="Move # thread"
                    other="Move # threads"
                  />
                }
                loading={loading}
                onCancel={close}
              />
            </ModalFooter>
          </Form>
        )
      }}
    </ThreadsModerationModal>
  )
}

export default ThreadsModerationModalMove
