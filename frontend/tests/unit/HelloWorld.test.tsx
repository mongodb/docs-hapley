import React from 'react';
import { render } from '@testing-library/react';
import HelloWorld from '../../src/components/HelloWorld';

describe('HelloWorld', () => {
  it('should render correctly', () => {
    const wrapper = render(<HelloWorld />);
    expect(wrapper.getByText('Hello World!')).toBeTruthy();
  });
});
