import React from "react"
import { RootContainer } from "../Storybook"
import RichText from "."

export default {
  title: "UI/RichText",
}

export const Paragraph = () => (
  <RootContainer>
    <RichText
      richText={[
        {
          id: "test",
          type: "p",
          text: "Lorem <strong>ipsum</strong> dolor met.",
        },
      ]}
    />
  </RootContainer>
)

export const Paragraphs = () => (
  <RootContainer>
    <RichText
      richText={[
        {
          id: "test1",
          type: "p",
          text: "Lorem <strong>ipsum</strong> dolor met.",
        },
        {
          id: "test2",
          type: "p",
          text: "Sit <em>amet</em> elit.",
        },
        {
          id: "test3",
          type: "p",
          text: 'Visit <a href="https://misago-project.org">Misago</a>!',
        },
      ]}
    />
  </RootContainer>
)

export const Headers = () => (
  <RootContainer>
    <RichText
      richText={[
        {
          id: "test1",
          type: "h1",
          text: "h1. Lorem <strong>ipsum</strong> dolor met.",
        },
        {
          id: "test2",
          type: "h2",
          text: "h2. Sit <em>amet</em> elit.",
        },
        {
          id: "test3",
          type: "h3",
          text: 'h3. Visit <a href="https://misago-project.org">Misago</a>!',
        },
        {
          id: "test4",
          type: "h4",
          text: "h4. Lorem <strong>ipsum</strong> dolor met.",
        },
        {
          id: "test5",
          type: "h5",
          text: "h5. Sit <em>amet</em> elit.",
        },
        {
          id: "test6",
          type: "h6",
          text: 'h6. Visit <a href="https://misago-project.org">Misago</a>!',
        },
      ]}
    />
  </RootContainer>
)

export const Quote = () => (
  <RootContainer>
    <RichText
      richText={[
        {
          id: "test",
          type: "quote",
          children: [
            {
              id: "test1",
              type: "p",
              text: "Lorem <strong>ipsum</strong> dolor met.",
            },
            {
              id: "test2",
              type: "p",
              text: "Sit <em>amet</em> elit.",
            },
          ],
        },
      ]}
    />
  </RootContainer>
)

export const Code = () => (
  <RootContainer>
    <RichText
      richText={[
        {
          id: "test",
          type: "code",
          syntax: "python",
          text: "print(hello)",
        },
      ]}
    />
  </RootContainer>
)

export const OrderedList = () => (
  <RootContainer>
    <RichText
      richText={[
        {
          id: "test",
          type: "list",
          ordered: true,
          children: [
            {
              id: "test1",
              type: "li",
              children: [
                {
                  id: "test2",
                  type: "f",
                  text: "Lorem <strong>ipsum</strong> dolor met.",
                },
              ],
            },
            {
              id: "test3",
              type: "li",
              children: [
                {
                  id: "test4",
                  type: "f",
                  text: "Sit amet elit.",
                },
              ],
            },
          ],
        },
      ]}
    />
  </RootContainer>
)

export const UnorderedList = () => (
  <RootContainer>
    <RichText
      richText={[
        {
          id: "test",
          type: "list",
          ordered: false,
          children: [
            {
              id: "test1",
              type: "li",
              children: [
                {
                  id: "test2",
                  type: "f",
                  text: "Lorem <strong>ipsum</strong> dolor met.",
                },
              ],
            },
            {
              id: "test3",
              type: "li",
              children: [
                {
                  id: "test4",
                  type: "f",
                  text: "Sit amet elit.",
                },
              ],
            },
          ],
        },
      ]}
    />
  </RootContainer>
)

export const NestedList = () => (
  <RootContainer>
    <RichText
      richText={[
        {
          id: "test",
          type: "list",
          ordered: false,
          children: [
            {
              id: "test1",
              type: "li",
              children: [
                {
                  id: "test2",
                  type: "f",
                  text: "Lorem <strong>ipsum</strong> dolor met.",
                },
                {
                  id: "test",
                  type: "list",
                  ordered: false,
                  children: [
                    {
                      id: "test1",
                      type: "li",
                      children: [
                        {
                          id: "test2",
                          type: "f",
                          text: "Lorem <strong>ipsum</strong> dolor met.",
                        },
                      ],
                    },
                    {
                      id: "test3",
                      type: "li",
                      children: [
                        {
                          id: "test4",
                          type: "f",
                          text: "Sit amet elit.",
                        },
                      ],
                    },
                  ],
                },
              ],
            },
            {
              id: "test3",
              type: "li",
              children: [
                {
                  id: "test4",
                  type: "f",
                  text: "Sit amet elit.",
                },
              ],
            },
          ],
        },
      ]}
    />
  </RootContainer>
)
