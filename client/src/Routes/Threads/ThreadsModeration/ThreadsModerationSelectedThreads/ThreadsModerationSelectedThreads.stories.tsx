import { action } from "@storybook/addon-actions"
import React from "react"
import { ButtonPrimary, Form } from "../../../../UI"
import { ModalFormContainer, categories } from "../../../../UI/Storybook"
import ThreadsModerationSelectedThreads from "./"
import { ISelectedThread } from "./ThreadsModerationSelectedThreads.types"

export default {
  title: "Route/Threads/Moderation/SelectedThreads",
}

interface IFormValues {
  threads: Array<ISelectedThread>
}

const submit = action("submit form")

export const SingleThread = () => {
  const threads = [
    {
      id: "1",
      title: "Nam id ante ultricies, laoreet leo tempor, venenatis ipsum.",
      replies: 719,
      category: Object.assign({}, categories[0].children[2], {
        parent: categories[0],
      }),
    },
  ]

  return (
    <Form<IFormValues> id="threads-select-test" onSubmit={submit}>
      <ModalFormContainer title="Threads moderation">
        <ThreadsModerationSelectedThreads max={10} min={1} threads={threads} />
        <ButtonPrimary text="Submit" block />
      </ModalFormContainer>
    </Form>
  )
}

export const FewThreads = () => {
  const threads = [
    {
      id: "1",
      title: "Nam id ante ultricies, laoreet leo tempor, venenatis ipsum.",
      replies: 719,
      category: Object.assign({}, categories[0].children[2], {
        parent: categories[0],
      }),
    },
    {
      id: "2",
      title: "Donec in tempor tellus.",
      replies: 0,
      category: Object.assign({}, categories[2]),
    },
  ]

  return (
    <Form<IFormValues> id="threads-select-test" onSubmit={submit}>
      <ModalFormContainer title="Threads moderation">
        <ThreadsModerationSelectedThreads max={10} min={1} threads={threads} />
        <ButtonPrimary text="Submit" block />
      </ModalFormContainer>
    </Form>
  )
}

export const ManyThreads = () => {
  const threads = [
    {
      id: "1",
      title: "Nam id ante ultricies, laoreet leo tempor, venenatis ipsum.",
      replies: 719,
      category: Object.assign({}, categories[0].children[2], {
        parent: categories[0],
      }),
    },
    {
      id: "2",
      title: "Donec in tempor tellus.",
      replies: 0,
      category: Object.assign({}, categories[2]),
    },
    {
      id: "3",
      title: "Integer iaculis ut tellus id lobortis.",
      replies: 12,
      category: Object.assign({}, categories[0].children[2], {
        parent: categories[0],
      }),
    },
  ]

  return (
    <Form<IFormValues> id="threads-select-test" onSubmit={submit}>
      <ModalFormContainer title="Threads moderation">
        <ThreadsModerationSelectedThreads max={10} min={1} threads={threads} />
        <ButtonPrimary text="Submit" block />
      </ModalFormContainer>
    </Form>
  )
}
