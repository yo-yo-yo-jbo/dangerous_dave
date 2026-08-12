import Head from "next/head";
import Comp from "./comp";

export default function Home() {
  return (
    <>
      <Head>
        <title>DAVE EDITOR</title>
        <meta name="description" content="Dave Editor" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
        <Comp />
    </>
  );
}
