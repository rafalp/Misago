import React from "react"
import posting from "../../services/posting"
import Button from "../button"
import { Toolbar, ToolbarItem, ToolbarSection, ToolbarSpacer } from "../Toolbar"
import ThreadsCategoryPicker from "./ThreadsCategoryPicker"
import ThreadsListPicker from "./ThreadsListPicker"
import ThreadsToolbarModeration from "./ThreadsToolbarModeration"

const ThreadsToolbar = ({
  api,
  baseUrl,
  category,
  categories,
  categoriesMap,
  topCategory,
  topCategories,
  subCategory,
  subCategories,
  list,
  lists,
  threads,
  addThreads,
  startThread,
  freezeThread,
  updateThread,
  deleteThread,
  selection,
  moderation,
  route,
  user,
  disabled,
}) => (
  <Toolbar>
    {topCategories.length > 0 && (
      <ToolbarSection>
        <ToolbarItem>
          <ThreadsCategoryPicker
            allItems={pgettext("threads list nav", "All categories")}
            parentUrl={list.path}
            category={topCategory}
            categories={topCategories}
            list={list}
          />
        </ToolbarItem>
        {topCategory && subCategories.length > 0 && (
          <ToolbarItem>
            <ThreadsCategoryPicker
              allItems={pgettext("threads list nav", "All subcategories")}
              parentUrl={topCategory.url.index}
              category={subCategory}
              categories={subCategories}
              list={list}
            />
          </ToolbarItem>
        )}
      </ToolbarSection>
    )}
    {lists.length > 1 && (
      <ToolbarSection className="hidden-xs">
        <ToolbarItem>
          <ThreadsListPicker baseUrl={baseUrl} list={list} lists={lists} />
        </ToolbarItem>
      </ToolbarSection>
    )}
    <ToolbarSpacer />
    {!!user.id && (
      <ToolbarSection>
        <ToolbarItem>
          <Button
            className="btn-primary btn-outline btn-block"
            disabled={disabled}
            onClick={() => {
              posting.open(
                startThread || {
                  mode: "START",

                  config: misago.get("THREAD_EDITOR_API"),
                  submit: misago.get("THREADS_API"),

                  category: category.id,
                }
              )
            }}
          >
            <span className="material-icon">chat</span>
            {pgettext("threads list nav", "Start thread")}
          </Button>
        </ToolbarItem>
        {!!moderation.allow && (
          <ToolbarItem shrink>
            <ThreadsToolbarModeration
              api={api}
              categories={categories}
              categoriesMap={categoriesMap}
              threads={threads.filter(
                (thread) => selection.indexOf(thread.id) !== -1
              )}
              addThreads={addThreads}
              freezeThread={freezeThread}
              updateThread={updateThread}
              deleteThread={deleteThread}
              selection={selection}
              moderation={moderation}
              route={route}
              user={user}
              disabled={disabled}
            />
          </ToolbarItem>
        )}
      </ToolbarSection>
    )}
  </Toolbar>
)

export default ThreadsToolbar
