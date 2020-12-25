import { Plural, Trans } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
import { useBulkActionLimit } from "../../../../Context"
import CategorySelect from "../../../../UI/CategorySelect"
import { Field, FieldError, Form, FormFooter } from "../../../../UI/Form"
import { ModalAlert, ModalFormBody, ModalFooter } from "../../../../UI/Modal"
import RootError from "../../../../UI/RootError"
import { CategoryValidationError } from "../../../../UI/ValidationError"
import { useSelectionErrors } from "../../../../UI/useSelectionErrors"
import { Thread } from "../../Threads.types"
import ThreadsModerationError from "../ThreadsModerationError"
import ThreadsModerationSelectedThreads from "../ThreadsModerationSelectedThreads"
import useMoveThreadsMutation from "./useMoveThreadsMutation"

interface ThreadsModerationMoveFormProps {
  threads: Array<Thread>
  close: () => void
}

interface FormValues {
  category: string
  threads: Array<Thread>
}

const ThreadsModerationMoveForm: React.FC<ThreadsModerationMoveFormProps> = ({
  threads,
  close,
}) => {
  const {
    errors: threadsErrors,
    clearErrors: clearThreadsErrors,
    setErrors: setThreadsErrors,
  } = useSelectionErrors<Thread>("threads")

  const {
    data,
    loading,
    moveThreads,
    error: graphqlError,
  } = useMoveThreadsMutation()

  const bulkActionLimit = useBulkActionLimit()
  const validators = Yup.object().shape({
    category: Yup.string().required("value_error.missing"),
    threads: Yup.array()
      .min(1, "value_error.list.min_items")
      .max(bulkActionLimit, "value_error.list.max_items"),
  })

  if (data && data.moveThreads.errors && data.moveThreads.updated) {
    return (
      <ThreadsModerationError
        errors={data.moveThreads.errors}
        threads={threads}
        close={close}
      />
    )
  }

  return (
    <Form<FormValues>
      id="move_threads_form"
      disabled={loading}
      defaultValues={{ threads, category: "" }}
      validators={validators}
      onSubmit={async ({
        clearErrors,
        setError,
        data: { category, threads },
      }) => {
        clearErrors()
        clearThreadsErrors()

        try {
          const result = await moveThreads(threads, category)
          const { errors } = result.data?.moveThreads || {}

          if (errors) {
            setThreadsErrors(threads, errors)
            errors?.forEach(({ location, type, message }) => {
              const field = location.join(".") as "category"
              setError(field, { type, message })
            })
          } else {
            close()
          }
        } catch (error) {
          // do nothing when moveThreads throws
          return
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
          max={bulkActionLimit}
          min={1}
          threads={threads}
        />
        <Field
          label={<Trans id="moderation.new_category">New category</Trans>}
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
}

export default ThreadsModerationMoveForm
