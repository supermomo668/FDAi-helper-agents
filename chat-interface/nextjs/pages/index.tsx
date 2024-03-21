// import {DeepChat as DeepChatCore} from 'deep-chat'; <- type
import {RequestDetails} from 'deep-chat/dist/types/interceptors';
import styles from '../styles/Index.module.css';
import dynamic from 'next/dynamic';
import { useEffect, useState } from 'react';

import Head from 'next/head';

// Styles for the DeepChat component
const chatStyles = {
  container: {
    borderRadius: "10px",
    border: "1px solid #e4e4e4",
    background: "linear-gradient(90deg, rgb(239, 242, 247) 0%, rgb(237, 240, 249) 15.2057%, ... , rgb(208, 224, 247) 100%)",
  },
  textInput: {
    styles: {
      container: {
        borderRadius: "20px",
        border: "unset",
        width: "78%",
        marginLeft: "-15px",
        boxShadow: "0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 1.6px 3.6px rgba(0, 0, 0, 0.16)",
      },
      text: {
        padding: "10px",
        paddingLeft: "15px",
        paddingRight: "34px",
      },
    },
    placeholder: {
      text: "Ask me anything...",
      style: { color: "#606060" },
    },
  },
  messageStyles: {
    default: {
      shared: {
        bubble: {
          backgroundColor: "unset",
          marginTop: "10px",
          marginBottom: "10px",
          boxShadow: "0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 1.6px 3.6px rgba(0, 0, 0, 0.16)",
        },
      },
      user: {
        bubble: {
          background: "linear-gradient(130deg, #2870EA 20%, #1B4AEF 77.5%)",
        },
      },
      ai: {
        bubble: {
          background: "rgba(255,255,255,0.7)",
        },
      },
    },
  },
  // Additional configurations (submitButtonStyles, microphone, etc.)
};

// Info to get a reference for the component:
// https://github.com/OvidijusParsiunas/deep-chat/issues/59#issuecomment-1839483469

// Info to add types to a component reference:
// https://github.com/OvidijusParsiunas/deep-chat/issues/59#issuecomment-1839487740

export default function IndexPage() {
  // Need to import the component dynamically as it uses the 'window' property.
  // If you have found a better way of adding the component in next, please create a new issue ticket so we can update the example!
  const DeepChat = dynamic(() => import('deep-chat-react').then((mod) => mod.DeepChat), {
    ssr: false,
  });
  const debugMode = process.env.NEXT_PUBLIC_DEBUG === 'true';
  console.log(`Debug Mode:${debugMode}`)
  const chatUrl = debugMode ? (process.env.NEXT_PUBLIC_DEBUG_BASE_URL || "http://localhost:3000"): (process.env.NEXT_PUBLIC_KHOJ_BASE_URL || "http://localhost:42110");

  return (
    <>
      <Head>
        <title>Chat with FDAi</title>
        <link rel="shortcut icon" href="public/static/favicon-128x128.ico" />
      </Head>
      <main className={styles.main}>
        <h1 id={styles.pageTitle}>
        </h1>
        <h1 className={styles.serverTitle}>Chat with FDAi</h1>
        <a href="https://fdai.earth/" target="_blank" rel="noreferrer" >
          <img 
            className={styles.serverTitleIcon} 
            src="https://i0.wp.com/fdai.earth/wp-content/uploads/2024/02/fdai-square-icon.png?fit=2000%2C2000&amp;ssl=1"
            decoding="async" srcSet="https://i0.wp.com/fdai.earth/wp-content/uploads/2024/02/fdai-square-icon.png?w=2000&amp;ssl=1 2000w, https://i0.wp.com/fdai.earth/wp-content/uploads/2024/02/fdai-square-icon.png?resize=300%2C300&amp;ssl=1 300w, https://i0.wp.com/fdai.earth/wp-content/uploads/2024/02/fdai-square-icon.png?resize=1024%2C1024&amp;ssl=1 1024w, https://i0.wp.com/fdai.earth/wp-content/uploads/2024/02/fdai-square-icon.png?resize=150%2C150&amp;ssl=1 150w, https://i0.wp.com/fdai.earth/wp-content/uploads/2024/02/fdai-square-icon.png?resize=768%2C768&amp;ssl=1 768w, https://i0.wp.com/fdai.earth/wp-content/uploads/2024/02/fdai-square-icon.png?resize=1536%2C1536&amp;ssl=1 1536w" style={{width: 50, marginBottom: '-1px'}}
            alt={"FDAi"}
          />
        </a>
        <div className={styles.components}>
          <div className={styles.diagonalLine} style={{background: '#e8f5ff'}}></div>
          {/* by setting maxMessages requestBodyLimits to 0 or lower - each request will send full chat history:
            https://deepchat.dev/docs/connect/#requestBodyLimits */}
          {/* If you don't want to or can't edit the target service, you can process the outgoing message using
            responseInterceptor and the incoming message using responseInterceptor:
            https://deepchat.dev/docs/interceptors */}
          <DeepChat
            style={{...chatStyles.container, width: '800px'}}
            introMessage={{text: 'Hi, I\'m a FDAi agent, please tell me your curious concerns about our project, health & longevity or anything!'}}
            stream={{ simulation: 60 }}
            request={{
              url: `${chatUrl}/api/chat/deepchat`,
              method: "POST",
              additionalBodyProps: {
                // "stream": "false",
                "n": 3,
                "client": "web",
                "conversation_id": 3,
                "region": "California",
                "city": "San Francisco",
                "country": "United States"
              },
              headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${process.env.NEXT_PUBLIC_KHOJ_API_TOKEN}`,
              }
            }}
            requestInterceptor={(details: RequestDetails) => {
              console.log(details);
              return details;
            }}
            responseInterceptor={(response: any) => {
              console.log(response);
              return response;
            }}
            audio={true}
            images={true}
            gifs={true}
            camera={true}
            microphone={true}
            mixedFiles={true}
            textInput={{placeholder: {text: 'Send a file!'}}}
            // validateInput={(_?: string, files?: File[]) => {
            //   return !!files && files.length > 0;
            // }}
            requestBodyLimits={{maxMessages: 1}}
            errorMessages={{displayServiceErrorMessages: true}}
          />
        </div>
        <h1 className={styles.serverTitle}>Chat with OpenAI</h1>
        <a href="https://openai.com/blog/openai-api" target="_blank" rel="noreferrer">
          <img
            className={styles.serverTitleIcon}
            src="https://raw.githubusercontent.com/OvidijusParsiunas/deep-chat/HEAD/website/static/img/openAILogo.png"
            style={{width: 26, marginBottom: '-1px'}}
            alt={'Title icon'}
          />
        </a>
        <div className={styles.components}>
          <div className={styles.diagonalLine} style={{background: '#f2f2f2'}}></div>
          {/* by setting maxMessages requestBodyLimits to 0 or lower - each request will send full chat history:
            https://deepchat.dev/docs/connect/#requestBodyLimits */}
          <DeepChat
            style={{borderRadius: '10px'}}
            introMessage={{text: 'Send a chat message to ask about OpenAI!'}}
            request={{url: '/api/openai/chat', additionalBodyProps: {model: 'gpt-3.5-turbo'}}}
            requestBodyLimits={{maxMessages: -1}}
            errorMessages={{displayServiceErrorMessages: true}}
          />
        </div>
      </main>
    </>
  );
}
