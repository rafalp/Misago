import React from "react"
import { ModalFormContainer, categories } from "../../../../UI/Storybook"
import ThreadsModerationSelectedThreads from "./"

export default {
  title: "Route/Threads/Moderation/SelectedThreads",
}

export const SingleThread = () => (
  <ModalFormContainer title="Threads moderation">
    <ThreadsModerationSelectedThreads
      threads={[
        {
          id: "1",
          title: "Nam id ante ultricies, laoreet leo tempor, venenatis ipsum.",
          replies: 719,
          category: Object.assign({}, categories[0].children[2], {
            parent: categories[0],
          }),
        },
      ]}
    />
  </ModalFormContainer>
)

export const FewThreads = () => (
  <ModalFormContainer title="Threads moderation">
    <ThreadsModerationSelectedThreads
      threads={[
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
      ]}
    />
  </ModalFormContainer>
)

export const ManyThreads = () => (
  <ModalFormContainer title="Threads moderation">
    <ThreadsModerationSelectedThreads
      threads={[
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
      ]}
    />
  </ModalFormContainer>
)
