// POC for Gatsby SSR: https://www.gatsbyjs.com/docs/how-to/custom-configuration/typescript/
// https://www.gatsbyjs.com/docs/how-to/rendering-options/using-server-side-rendering/
import * as React from 'react';
import type { GetServerDataReturn, PageProps } from 'gatsby';
import { Link } from 'gatsby';

interface DogData {
  message: string;
  status: string;
}

type ServerDataProps = {
  dogImage: DogData;
};

const SSRPOC = (props: PageProps<undefined, undefined, undefined, ServerDataProps>) => {
  const { serverData } = props;
  return (
    <main>
      <Link to="/">Go back to the homepage</Link>
      <h1>SSR POC</h1>
      <p>Reload the page to see the dog image change!</p>
      <img alt="Happy dog" src={serverData.dogImage.message} />
    </main>
  );
};

export default SSRPOC;

export async function getServerData(): GetServerDataReturn<ServerDataProps> {
  try {
    const res = await fetch(`https://dog.ceo/api/breeds/image/random`);
    if (!res.ok) {
      throw new Error(`Response failed`);
    }
    const data = await res.json();
    return {
      props: {
        dogImage: data
      }
    };
  } catch (error) {
    return {
      status: 500,
      headers: {}
    };
  }
}
