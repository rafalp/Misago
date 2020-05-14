import { Plural, Trans } from "@lingui/macro"
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
  Spinner,
} from "../../../UI"
import ThreadsModerationModal from "./ThreadsModerationModal"
import { ThreadsModerationModalAction } from "./ThreadsModerationModalContext"
import ThreadsModerationModalThreadsList from "./ThreadsModerationModalThreadsList"
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
              <ThreadsModerationModalThreadsList threads={threads} />
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
              <Spinner small />
              <ButtonSecondary
                text={<Trans id="cancel">Cancel</Trans>}
                disabled={loading}
                responsive
                onClick={close}
              />
              <ButtonPrimary
                text={
                  <Plural
                    id="moderation.move_threads.submit"
                    value={threads.length}
                    one="Move # thread"
                    other="Move # threads"
                  />
                }
                disabled={loading}
                responsive
              />
            </ModalFooter>
          </Form>
        )
      }}
    </ThreadsModerationModal>
  )
}

export default ThreadsModerationModalMove
