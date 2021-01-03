import { action } from "@storybook/addon-actions"
import { withKnobs, text } from "@storybook/addon-knobs"
import React from "react"
import { RootContainer, userFactory } from "../../../UI/Storybook"
import ThreadPost from "./ThreadPost"

export default {
  title: "Route/Thread/Post",
  decorators: [withKnobs],
}

export const PostByUser = () => {
  const username = text("Poster name", "John")

  return (
    <RootContainer>
      <ThreadPost
        post={{
          id: "1",
          richText: [
            {
              id: "aaaa",
              type: "p",
              text: "Lorem ipsum dolor met sit amet elit.",
            },
          ],
          edits: 0,
          postedAt: "2020-04-01T21:42:51Z",
          posterName: username,
          poster: userFactory({ name: username }),
          extra: {},
        }}
        threadId="1"
        threadSlug="test-thread"
      />
    </RootContainer>
  )
}

export const PostWithComplexMarkup = () => {
  const username = text("Poster name", "John")

  return (
    <RootContainer>
      <ThreadPost
        post={{
          id: "1",
          richText: [
            {
              id: "FRAsvaGJO8",
              type: "h1",
              text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            },
            {
              id: "j9txbaKTrV",
              type: "p",
              text:
                "Praesent finibus consequat eros. <strong>Phasellus ut eleifend orci.</strong> Aliquam erat volutpat. Vestibulum porttitor, sem quis mattis placerat, <em>enim neque aliquam leo</em>, id porta elit ante ut justo.",
            },
            {
              id: "Ejg53h02ey",
              type: "p",
              text:
                'Suspendisse enim massa, rutrum eget bibendum a, <a href="http://misago-project.org">porttitor vitae</a> turpis. Aliquam erat volutpat. Duis dapibus sapien nunc.',
            },
            {
              id: "SahFev4iYA",
              type: "h2",
              text: "Duis dapibus sapien nunc.",
            },
            {
              id: "MM5QvSv6kx",
              type: "p",
              text:
                "Praesent ultrices, massa eu mollis iaculis, sapien magna fringilla ante, sed tristique neque ipsum quis purus.",
            },
            {
              id: "70DhUN9iVC",
              type: "quote",
              author: null,
              post: null,
              children: [
                {
                  id: "ATKzQGt5MK",
                  type: "p",
                  text:
                    "Duis commodo purus a tortor accumsan, vitae fermentum sem viverra:",
                },
                {
                  id: "wWrkdSR4Uw",
                  type: "p",
                  text: '<img src="https://placekitten.com/200/300" alt=""/>',
                },
                {
                  id: "9KgFC4x11w",
                  type: "quote",
                  author: null,
                  post: null,
                  children: [
                    {
                      id: "mvpcGyQI9B",
                      type: "p",
                      text:
                        "Sed aliquet tristique sollicitudin. Pellentesque vestibulum porta consequat. Morbi in ante turpis. Maecenas non dui sapien. Sed gravida arcu non enim posuere tristique.",
                    },
                    {
                      id: "mvpcGyQI9B",
                      type: "hr",
                    },
                    {
                      id: "nqVDbWYILr",
                      type: "p",
                      text:
                        "Fusce ut ligula nec tortor auctor volutpat. Nam in nibh rutrum ligula tristique vulputate.",
                    },
                  ],
                },
                {
                  id: "aZKbQlWbHV",
                  type: "p",
                  text:
                    "Mauris convallis enim lectus, malesuada iaculis nisl iaculis nec. Proin sit amet efficitur dolor. Phasellus sollicitudin nec odio ac posuere!",
                },
              ],
            },
          ],
          edits: 0,
          postedAt: "2020-04-01T21:42:51Z",
          posterName: username,
          poster: userFactory({ name: username }),
          extra: {},
        }}
        threadId="1"
        threadSlug="test-thread"
      />
    </RootContainer>
  )
}

export const PostWithQuotes = () => (
  <RootContainer>
    <ThreadPost
      post={{
        id: "1",
        richText: [
          {
            id: "7QBDrdY5KB",
            type: "p",
            text: "Quote without author within quote without author:",
          },
          {
            id: "70DhUN9iVC",
            type: "quote",
            author: null,
            post: null,
            children: [
              {
                id: "ATKzQGt5MK",
                type: "p",
                text:
                  'Duis commodo purus a tortor accumsan, <a href="http://misago-project.org">vitae</a> fermentum sem viverra:',
              },
              {
                id: "9KgFC4x11w",
                type: "quote",
                author: null,
                post: null,
                children: [
                  {
                    id: "mvpcGyQI9B",
                    type: "p",
                    text:
                      "Sed aliquet tristique sollicitudin. Pellentesque vestibulum porta consequat. Morbi in ante turpis. Maecenas non dui sapien. Sed gravida arcu non enim posuere tristique.",
                  },
                  {
                    id: "mvpcGyQI9B",
                    type: "hr",
                  },
                  {
                    id: "nqVDbWYILr",
                    type: "p",
                    text:
                      "Fusce ut ligula nec tortor auctor volutpat. Nam in nibh rutrum ligula tristique vulputate.",
                  },
                ],
              },
              {
                id: "aZKbQlWbHV",
                type: "p",
                text:
                  "Mauris convallis enim lectus, malesuada iaculis nisl iaculis nec. Proin sit amet efficitur dolor. Phasellus sollicitudin nec odio ac posuere!",
              },
            ],
          },
          {
            id: "2fQ6m3ch3l",
            type: "p",
            text:
              "Quote with existing author within quote with existing author:",
          },
          {
            id: "fdJuQmMKSo",
            type: "quote",
            author: { id: 1, name: "Alice", slug: "alice" },
            post: null,
            children: [
              {
                id: "ATKzQGt5MK",
                type: "p",
                text:
                  'Duis commodo purus a tortor accumsan, <a href="http://misago-project.org">vitae</a> fermentum sem viverra:',
              },
              {
                id: "9KgFC4x11w",
                type: "quote",
                author: { id: 2, name: "Jane", slug: "jane" },
                post: null,
                children: [
                  {
                    id: "mvpcGyQI9B",
                    type: "p",
                    text:
                      "Sed aliquet tristique sollicitudin. Pellentesque vestibulum porta consequat. Morbi in ante turpis. Maecenas non dui sapien. Sed gravida arcu non enim posuere tristique.",
                  },
                  {
                    id: "mvpcGyQI9B",
                    type: "hr",
                  },
                  {
                    id: "nqVDbWYILr",
                    type: "p",
                    text:
                      "Fusce ut ligula nec tortor auctor volutpat. Nam in nibh rutrum ligula tristique vulputate.",
                  },
                ],
              },
              {
                id: "aZKbQlWbHV",
                type: "p",
                text:
                  "Mauris convallis enim lectus, malesuada iaculis nisl iaculis nec. Proin sit amet efficitur dolor. Phasellus sollicitudin nec odio ac posuere!",
              },
            ],
          },
          {
            id: "q2sX8WmmWt",
            type: "p",
            text:
              "Quote with anonymous author within quote with anonymous author:",
          },
          {
            id: "mpZwkAbwgt",
            type: "quote",
            author: { id: null, name: "Alice", slug: null },
            post: null,
            children: [
              {
                id: "ATKzQGt5MK",
                type: "p",
                text:
                  'Duis commodo purus a tortor accumsan, <a href="http://misago-project.org">vitae</a> fermentum sem viverra:',
              },
              {
                id: "9KgFC4x11w",
                type: "quote",
                author: { id: null, name: "Jane", slug: null },
                post: null,
                children: [
                  {
                    id: "mvpcGyQI9B",
                    type: "p",
                    text:
                      "Sed aliquet tristique sollicitudin. Pellentesque vestibulum porta consequat. Morbi in ante turpis. Maecenas non dui sapien. Sed gravida arcu non enim posuere tristique.",
                  },
                  {
                    id: "mvpcGyQI9B",
                    type: "hr",
                  },
                  {
                    id: "nqVDbWYILr",
                    type: "p",
                    text:
                      "Fusce ut ligula nec tortor auctor volutpat. Nam in nibh rutrum ligula tristique vulputate.",
                  },
                ],
              },
              {
                id: "aZKbQlWbHV",
                type: "p",
                text:
                  "Mauris convallis enim lectus, malesuada iaculis nisl iaculis nec. Proin sit amet efficitur dolor. Phasellus sollicitudin nec odio ac posuere!",
              },
            ],
          },
          {
            id: "uKAvPXLjpp",
            type: "p",
            text:
              "Quote with author and post within quote with author and post:",
          },
          {
            id: "nZ3kaWPJ3Z",
            type: "quote",
            author: { id: null, name: "Alice", slug: null },
            post: 123,
            children: [
              {
                id: "ATKzQGt5MK",
                type: "p",
                text:
                  'Duis commodo purus a tortor accumsan, <a href="http://misago-project.org">vitae</a> fermentum sem viverra:',
              },
              {
                id: "9KgFC4x11w",
                type: "quote",
                author: { id: null, name: "Jane", slug: null },
                post: 123,
                children: [
                  {
                    id: "mvpcGyQI9B",
                    type: "p",
                    text:
                      "Sed aliquet tristique sollicitudin. Pellentesque vestibulum porta consequat. Morbi in ante turpis. Maecenas non dui sapien. Sed gravida arcu non enim posuere tristique.",
                  },
                  {
                    id: "mvpcGyQI9B",
                    type: "hr",
                  },
                  {
                    id: "nqVDbWYILr",
                    type: "p",
                    text:
                      "Fusce ut ligula nec tortor auctor volutpat. Nam in nibh rutrum ligula tristique vulputate.",
                  },
                ],
              },
              {
                id: "aZKbQlWbHV",
                type: "p",
                text:
                  "Mauris convallis enim lectus, malesuada iaculis nisl iaculis nec. Proin sit amet efficitur dolor. Phasellus sollicitudin nec odio ac posuere!",
              },
            ],
          },
          {
            id: "XbuJwGNVSA",
            type: "p",
            text: "Quote within spoiler block:",
          },
          {
            id: "ZYJW7M8FAY",
            type: "spoiler",
            children: [
              {
                id: "9KgFC4x11w",
                type: "quote",
                author: { id: null, name: "Jane", slug: null },
                post: 123,
                children: [
                  {
                    id: "mvpcGyQI9B",
                    type: "p",
                    text:
                      "Sed aliquet tristique sollicitudin. Pellentesque vestibulum porta consequat. Morbi in ante turpis. Maecenas non dui sapien. Sed gravida arcu non enim posuere tristique.",
                  },
                  {
                    id: "mvpcGyQI9B",
                    type: "hr",
                  },
                  {
                    id: "nqVDbWYILr",
                    type: "p",
                    text:
                      "Fusce ut ligula nec tortor auctor volutpat. Nam in nibh rutrum ligula tristique vulputate.",
                  },
                ],
              },
            ],
          },
        ],
        edits: 0,
        postedAt: "2020-04-01T21:42:51Z",
        posterName: "John",
        poster: userFactory({ name: "John" }),
        extra: {},
      }}
      threadId="1"
      threadSlug="test-thread"
    />
  </RootContainer>
)

export const PostWithSpoilers = () => (
  <RootContainer>
    <ThreadPost
      post={{
        id: "1",
        richText: [
          {
            id: "7QBDrdY5KB",
            type: "p",
            text: "Spoiler:",
          },
          {
            id: "70DhUN9iVC",
            type: "spoiler",
            children: [
              {
                id: "mvpcGyQI9B",
                type: "p",
                text:
                  "Sed aliquet tristique sollicitudin. Pellentesque vestibulum porta consequat. Morbi in ante turpis. Maecenas non dui sapien. Sed gravida arcu non enim posuere tristique.",
              },
              {
                id: "mvpcGyQI9B",
                type: "hr",
              },
              {
                id: "nqVDbWYILr",
                type: "p",
                text:
                  "Fusce ut ligula nec tortor auctor volutpat. Nam in nibh rutrum ligula tristique vulputate.",
              },
            ],
          },
          {
            id: "2fQ6m3ch3l",
            type: "p",
            text: "Spoiler within quote:",
          },
          {
            id: "fdJuQmMKSo",
            type: "quote",
            author: { id: 1, name: "Alice", slug: "alice" },
            post: null,
            children: [
              {
                id: "9KgFC4x11w",
                type: "spoiler",
                children: [
                  {
                    id: "mvpcGyQI9B",
                    type: "p",
                    text:
                      "Sed aliquet tristique sollicitudin. Pellentesque vestibulum porta consequat. Morbi in ante turpis. Maecenas non dui sapien. Sed gravida arcu non enim posuere tristique.",
                  },
                  {
                    id: "mvpcGyQI9B",
                    type: "hr",
                  },
                  {
                    id: "nqVDbWYILr",
                    type: "p",
                    text:
                      "Fusce ut ligula nec tortor auctor volutpat. Nam in nibh rutrum ligula tristique vulputate.",
                  },
                ],
              },
            ],
          },
          {
            id: "q2sX8WmmWt",
            type: "p",
            text: "Spoiler within spoiler:",
          },
          {
            id: "mpZwkAbwgt",
            type: "spoiler",
            children: [
              {
                id: "ATKzQGt5MK",
                type: "p",
                text:
                  'Duis commodo purus a tortor accumsan, <a href="http://misago-project.org">vitae</a> fermentum sem viverra:',
              },
              {
                id: "9KgFC4x11w",
                type: "spoiler",
                children: [
                  {
                    id: "mvpcGyQI9B",
                    type: "p",
                    text:
                      "Sed aliquet tristique sollicitudin. Pellentesque vestibulum porta consequat. Morbi in ante turpis. Maecenas non dui sapien. Sed gravida arcu non enim posuere tristique.",
                  },
                  {
                    id: "mvpcGyQI9B",
                    type: "hr",
                  },
                  {
                    id: "nqVDbWYILr",
                    type: "p",
                    text:
                      "Fusce ut ligula nec tortor auctor volutpat. Nam in nibh rutrum ligula tristique vulputate.",
                  },
                ],
              },
              {
                id: "aZKbQlWbHV",
                type: "p",
                text:
                  "Mauris convallis enim lectus, malesuada iaculis nisl iaculis nec. Proin sit amet efficitur dolor. Phasellus sollicitudin nec odio ac posuere!",
              },
            ],
          },
        ],
        edits: 0,
        postedAt: "2020-04-01T21:42:51Z",
        posterName: "John",
        poster: userFactory({ name: "John" }),
        extra: {},
      }}
      threadId="1"
      threadSlug="test-thread"
    />
  </RootContainer>
)

export const PostWithCode = () => (
  <RootContainer>
    <ThreadPost
      post={{
        id: "1",
        richText: [
          {
            id: "7QBDrdY5KB",
            type: "p",
            text: "Code:",
          },
          {
            id: "70DhUN9iVC",
            type: "code",
            syntax: null,
            text: "do_something(user_obj);",
          },
          {
            id: "2fQ6m3ch3l",
            type: "p",
            text: "Code within quote:",
          },
          {
            id: "fdJuQmMKSo",
            type: "quote",
            author: { id: 1, name: "Alice", slug: "alice" },
            post: null,
            children: [
              {
                id: "70DhUN9iVC",
                type: "code",
                syntax: null,
                text: "do_something(user_obj);",
              },
            ],
          },
          {
            id: "q2sX8WmmWt",
            type: "p",
            text: "Code within spoiler:",
          },
          {
            id: "mpZwkAbwgt",
            type: "spoiler",
            children: [
              {
                id: "70DhUN9iVC",
                type: "code",
                syntax: null,
                text: "do_something(user_obj);",
              },
            ],
          },
        ],
        edits: 0,
        postedAt: "2020-04-01T21:42:51Z",
        posterName: "John",
        poster: userFactory({ name: "John" }),
        extra: {},
      }}
      threadId="1"
      threadSlug="test-thread"
    />
  </RootContainer>
)

export const PostSelectable = () => {
  const username = text("Poster name", "John")

  return (
    <RootContainer>
      <ThreadPost
        post={{
          id: "1",
          richText: [
            {
              id: "aaaa",
              type: "p",
              text: "Lorem ipsum dolor met sit amet elit.",
            },
          ],
          edits: 0,
          postedAt: "2020-04-01T21:42:51Z",
          posterName: username,
          poster: userFactory({ name: username }),
          extra: {},
        }}
        threadId="1"
        threadSlug="test-thread"
        isSelected={false}
        toggleSelection={action("Toggle selection")}
      />
    </RootContainer>
  )
}

export const PostByDeletedUser = () => {
  const username = text("Poster name", "John")

  return (
    <RootContainer>
      <ThreadPost
        post={{
          id: "1",
          richText: [
            {
              id: "aaaa",
              type: "p",
              text: "Lorem ipsum dolor met sit amet elit.",
            },
          ],
          edits: 0,
          postedAt: "2020-04-01T21:42:51Z",
          posterName: username,
          poster: null,
          extra: {},
        }}
        threadId="1"
        threadSlug="test-thread"
      />
    </RootContainer>
  )
}

export const PostAfterAnother = () => (
  <RootContainer>
    <ThreadPost
      post={{
        id: "1",
        richText: [
          {
            id: "aaaa",
            type: "p",
            text: "Lorem ipsum dolor met sit amet elit.",
          },
        ],
        edits: 0,
        postedAt: "2020-04-01T21:42:51Z",
        posterName: "John",
        poster: null,
        extra: {},
      }}
      threadId="1"
      threadSlug="test-thread"
    />
    <ThreadPost
      post={{
        id: "2",
        richText: [
          {
            id: "bbbb",
            type: "p",
            text: "Lorem ipsum dolor met sit amet elit.",
          },
        ],
        edits: 0,
        postedAt: "2020-04-03T15:22:11Z",
        posterName: "Doe",
        poster: null,
        extra: {},
      }}
      threadId="1"
      threadSlug="test-thread"
    />
  </RootContainer>
)
