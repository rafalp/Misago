import { Trans } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
import {
  CategorySelect,
  CategoryValidationError,
  Field,
  FieldError,
  Form,
  FormFooter,
  ModalAlert,
  ModalFormBody,
  ModalFooter,
} from "../../../../UI"
import { IThread } from "../../Thread.types"
import ThreadRootError from "../../ThreadRootError"
import useMoveThreadMutation from "../moveThread"

interface IThreadModerationMoveFormProps {
  thread: IThread
  close: () => void
}

interface IFormValues {
  category: string
}

const ThreadModerationMoveForm: React.FC<IThreadModerationMoveFormProps> = ({
  thread,
  close,
}) => {
  const {
    data,
    loading,
    moveThread,
    error: graphqlError,
  } = useMoveThreadMutation()

  const MoveThreadSchema = Yup.object().shape({
    category: Yup.string().required("value_error.missing"),
  })

  return (
    <Form<IFormValues>
      id="move_thread_form"
      disabled={loading}
      defaultValues={{ category: "" }}
      validationSchema={MoveThreadSchema}
      onSubmit={async ({ clearError, setError, data: { category } }) => {
        clearError()

        try {
          const result = await moveThread(thread, category)
          const { errors } = result.data?.moveThread || {}

          if (errors) {
            errors?.forEach(({ location, type, message }) => {
              const field = location.join(".")
              setError(field, type, message)
            })
          } else {
            close()
          }
        } catch (error) {
          // do nothing when moveThread throws
          return
        }
      }}
    >
      <ThreadRootError
        graphqlError={graphqlError}
        dataErrors={data?.moveThread.errors}
      >
        {({ message }) => <ModalAlert>{message}</ModalAlert>}
      </ThreadRootError>
      <ModalFormBody>
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
            <Trans id="moderation.move_thread.submit">Move thread</Trans>
          }
          loading={loading}
          onCancel={close}
        />
      </ModalFooter>
    </Form>
  )
}

export default ThreadModerationMoveForm
