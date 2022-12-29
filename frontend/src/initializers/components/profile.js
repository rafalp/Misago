import { connect } from "react-redux"
import Profile, { paths, select } from "misago/components/profile/root"
import misago from "misago/index"
import mount from "misago/utils/routed-component"

export default function initializer(context) {
  if (context.has("PROFILE") && context.has("PROFILE_PAGES")) {
    mount({
      root: misago.get("PROFILE").url,
      component: connect(select)(Profile),
      paths: paths(),
    })
  }
}

misago.addInitializer({
  name: "component:profile",
  initializer: initializer,
  after: "reducer:profile-hydrate",
})
