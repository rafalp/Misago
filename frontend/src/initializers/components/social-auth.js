// jshint ignore:start
import React from 'react';
import SocialAuth from 'misago/components/social-auth';
import misago from 'misago';
import mount from 'misago/utils/mount-component';

export default function initializer(context) {
  if (context.get('CURRENT_LINK') === 'social:complete') {
    const props = context.get('SOCIAL_AUTH');
    mount(<SocialAuth {...props} />, 'page-mount');
  }
}

misago.addInitializer({
  name: 'component:social-auth',
  initializer: initializer,
  after: 'store'
});
