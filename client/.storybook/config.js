import { configure } from '@storybook/react';
import requireContext from 'require-context.macro';

import '../src/styles/index.scss';

// automatically import all files ending in *.stories.js
configure(requireContext('../src/', true, /\.stories\.tsx$/), module);
