import { Trans } from "@lingui/macro"
import React from "react"
import { useCategoriesListContext } from "../../../Context"
import {
  ButtonPrimary,
  ButtonSecondary,
  Field,
  Form,
  ModalAlert,
  ModalFormBody,
  ModalFooter,
  RootError,
  Select,
} from "../../../UI"
import ThreadsModerationModal from "./ThreadsModerationModal"
import { ThreadsModerationModalAction } from "./ThreadsModerationModalContext"
import useMoveThreadsMutation from "./moveThreads"

interface IFormValues {
  category?: string
}

const ThreadsModerationModalMove: React.FC = () => {
  const categories = useCategoriesListContext()
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
      {({ threads, close }) => {
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
              <ul>
                {threads.map((thread) => (
                  <li key={thread.id}>{thread.title}</li>
                ))}
              </ul>
              <Field
                label={
                  <Trans id="moderation.new_category">New category</Trans>
                }
                name="category"
                input={
                  <Select
                    options={categories.map(({ category, depth }) => {
                      return {
                        value: category.id,
                        name: depth ? "-   " + category.name : category.name,
                      }
                    })}
                  />
                }
              />
            </ModalFormBody>
            <ModalFooter>
              <ButtonSecondary
                text="cancel"
                disabled={loading}
                responsive
                onClick={close}
              />
              <ButtonPrimary text="move" loading={loading} responsive />
            </ModalFooter>
          </Form>
        )
      }}
    </ThreadsModerationModal>
  )
}

export default ThreadsModerationModalMove
