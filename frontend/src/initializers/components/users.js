import misago from "misago/index"
import Users, { paths } from "../../components/users/root"
import mount from "../../utils/routed-component"

export default function initializer(context) {
  if (context.has("USERS_LISTS")) {
    mount({
      basepath: misago.get("USERS_LIST_URL"),
      component: Users,
      paths: paths(),
    })
  }
}

misago.addInitializer({
  name: "component:users",
  initializer: initializer,
  after: "store",
})
