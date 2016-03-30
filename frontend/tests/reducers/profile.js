import assert from 'assert';
import moment from 'moment';
import { StoreWrapper } from 'misago/services/store';
import { updateAvatar, updateUsername } from 'misago/reducers/users';
import reducer, { hydrate, patch } from 'misago/reducers/profile';

let profileMock = null;
let store = null;

describe("Profile Reducer", function() {
  beforeEach(function() {
    profileMock = {
      id: 42,
      username: "BobBoberson",
      email: 'sadsa@sda.com',
      avatar_hash: 'aabbccdd',

      joined_on: moment().format(),

      title: '',
      rank: {
        id: 321,
        name: "Test Rank",
        slug: "test-rank",
        css_class: '',
        is_tab: false,
        title: ''
      },

      status: {
        last_click: moment().format(),
        banned_until: null
      },

      is_followed: false,

      acl: {
        can_follow: false,
        can_moderate: false
      }
    };

    store = new StoreWrapper();
    store.addReducer('profile', reducer, {});
    store.init();
  });

  it("hydrate action hydrates user profile", function() {
    let joinedOn = moment().format();
    profileMock.joined_on = joinedOn;

    let lastClick = moment().format();
    profileMock.joined_on = lastClick;

    store.dispatch(hydrate(profileMock));
    let profile = store.getState().profile;

    assert.equal(profile.joined_on.format(), joinedOn,
      "joined_on date becomes moment() object");
    assert.equal(profile.status.last_click.format(), lastClick,
      "user status is hydrated too");
    assert.equal(profile.id, profileMock.id, "other keys are preserved");
  });

  it("patch action updates user profile", function() {
    store.dispatch(hydrate(profileMock));
    store.dispatch(patch({
      'email': 'yolo@test.com',
      'lorem': 'ipsum'
    }));

    let profile = store.getState().profile;
    assert.equal(profile.email, 'yolo@test.com',
      "existing property was patched");
    assert.equal(profile.lorem, 'ipsum',
      "new property was patched in");
  });

  it("updateAvatar updates profile avatar", function() {
    store.dispatch(hydrate(profileMock));
    store.dispatch(updateAvatar(profileMock, 'new-hash'));

    let profile = store.getState().profile;
    assert.equal(profile.avatar_hash, 'new-hash',
      "avatar hash was updated for profile user");

    store.dispatch(updateAvatar({id: 1}, 'other-hash'));

    profile = store.getState().profile;
    assert.equal(profile.avatar_hash, 'new-hash',
      "profile reducer tests id for avatar change");
  });

  it("updateUsername updates profile username", function() {
    store.dispatch(hydrate(profileMock));
    store.dispatch(updateUsername(profileMock, 'RenamedUser', 'renameduser'));

    let profile = store.getState().profile;
    assert.equal(profile.username, 'RenamedUser',
      "profile username was updated");
    assert.equal(profile.slug, 'renameduser',
      "profile slug was updated");

    store.dispatch(updateUsername({id: 1}, 'OtherRename', 'otherrename'));

    profile = store.getState().profile;
    assert.equal(profile.username, 'RenamedUser',
      "profile reducer tests id for username change");
  });
});