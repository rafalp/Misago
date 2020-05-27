import { Plural, Trans } from "@lingui/macro"
import React from "react"
import {
  CategorySelect,
  Field,
  Form,
  FormFooter,
  ModalAlert,
  ModalFormBody,
  ModalFooter,
  RootError,
} from "../../../UI"
import ThreadsModerationModal from "./ThreadsModerationModal"
import { ThreadsModerationModalAction } from "./ThreadsModerationModalContext"
import ThreadsModerationSelectedThreads from "./ThreadsModerationSelectedThreads"
import useMoveThreadsMutation from "./moveThreads"

interface IFormValues {
  category?: string
}

const ThreadsModerationModalMove: React.FC = () => {
  const {
    data,
    loading,
    moveThreads,
    error: graphqlError,
  } = useMoveThreadsMutation()
  const [error, setError] = React.useState<string | null>(null)

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
            onSubmit={async ({ data: { category } }) => {
              if (!category) {
                setError("value_error.all_fields_are_required")
                return
              }

              setError(null)
              const data = await moveThreads(threads, category)
              const { errors } = data.data?.moveThreads || {}
              if (!errors) close()
            }}
          >
            <RootError
              graphqlError={graphqlError}
              dataErrors={data?.moveThreads.errors}
              plainError={error}
            >
              {({ message }) => <ModalAlert>{message}</ModalAlert>}
            </RootError>
            <ModalFormBody>
              <ThreadsModerationSelectedThreads threads={threads} />
              <Field
                label={
                  <Trans id="moderation.new_category">New category</Trans>
                }
                name="category"
                input={<CategorySelect />}
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
