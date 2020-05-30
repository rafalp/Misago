import { Plural, Trans } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
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
import { IThread } from "../Threads.types"
import ThreadsModerationModal from "./ThreadsModerationModal"
import { ThreadsModerationModalAction } from "./ThreadsModerationModalContext"
import ThreadsModerationSelectedThreads from "./ThreadsModerationSelectedThreads"
import useMoveThreadsMutation from "./moveThreads"

interface IFormValues {
  category?: string
  threads?: Array<IThread>
}

const ThreadsModerationModalMove: React.FC = () => {
  const {
    data,
    loading,
    moveThreads,
    error: graphqlError,
  } = useMoveThreadsMutation()

  const MoveThreadsSchema = Yup.object().shape({
    category: Yup.string().required("value_error.missing"),
    threads: Yup.string().required("value_error.missing"),
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
            defaultValues={{ threads }}
            validationSchema={MoveThreadsSchema}
            onSubmit={async ({
              clearError,
              setError,
              data: { category, threads },
            }) => {
              if (!category || !threads) return

              clearError()

              const data = await moveThreads(threads, category)
              const { errors } = data.data?.moveThreads || {}
              if (errors) {
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
