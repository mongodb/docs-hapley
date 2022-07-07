import * as React from 'react';
import { Link } from 'gatsby';

// styles
const pageStyles = {
  color: '#232129',
  padding: 96,
  fontFamily: '-apple-system, Roboto, sans-serif, serif'
};
const headingStyles = {
  marginTop: 0,
  marginBottom: 64,
  maxWidth: 320
};
const headingAccentStyles = {
  color: '#663399'
};
const paragraphStyles = {
  marginBottom: 48
};
const codeStyles = {
  color: '#8A6534',
  padding: 4,
  backgroundColor: '#FFF4DB',
  fontSize: '1.25rem',
  borderRadius: 4
};

function IndexPage() {
  return (
    <main style={pageStyles}>
      <title>Hapley</title>
      <h1 style={headingStyles}>
        Congratulations
        <br />
        <span style={headingAccentStyles}> Welcome to Hapley! </span>
        🎉🎉🎉
      </h1>
      <p style={paragraphStyles}>
        Edit <code style={codeStyles}>src/pages/index.tsx</code> to see this page update in
        real-time. 😎
      </p>
      <p>
        See the POC for SSR <Link to="/ssr-poc"> here</Link>.
      </p>
    </main>
  );
}

export default IndexPage;
