import React, { useState, useEffect, useRef } from 'react';
// import { ReactMic } from 'react-mic';
import Typewriter from 'typewriter-effect';
import socketIOClient from 'socket.io-client';
import "./styles.css";

enum MessageType {
  Text,
  Audio
}

interface Body {
  type: MessageType,
  data: string
}

interface ChatMessage {
  author: string,
  body: Body,
  timeout: number
}

const initialMessages: ChatMessage[] = [
  {
    author: 'bot',
    body: { type: MessageType.Text, data: 'Hello there. How can we help?' },
    timeout: 800
  }
];

const Message = ({ data }: { data: ChatMessage }) => {
  const { author, body } = data;
  console.log(data);
  let finalBody;

  if (Array.isArray(body)) {
    finalBody = body.map((item, index) => (
      <React.Fragment key={index}>
        {item === "..." && (
          <div className="typing">
            <span></span>
            <span></span>
            <span></span>
          </div>
        )}
        {item !== "..." && (
          <a href={item.url} className="c-chat__action" key={index}>
            {item.text}
          </a>
        )}
      </React.Fragment>
    ));
  } else {
    if (body.type === MessageType.Text) {
      if (body.data === "...") {
        finalBody = (
          <div className="c-chat__message typing">
            <span></span>
            <span></span>
            <span></span>
          </div>
        );
      } else {
        if (author === "bot") {
          finalBody = (
            <div className="c-chat__message">
              <Typewriter
                options={{
                  strings: body.data,
                  autoStart: true,
                  delay: 5,
                  loop: false,
                }}
              />
            </div>
          );
        } else {
          finalBody = <div className="c-chat__message"> {body.data} </div>;
        }
      }
    } else {
      finalBody = <div><audio controls>
        <source src={body.data} type="audio/wav" />
        Your browser does not support the audio element.
      </audio></div>;
    }
  }

  return (
    <li className={`c-chat__item c-chat__item--${author}`}>{finalBody}</li>
  );
};

const Chat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [questionSubmitted, setQuestionSubmitted] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [recordedAudio, setRecordedAudio] = useState<any>(null);
  const mediaRecorder = useRef<any>(null);

  const socket = socketIOClient('http://localhost:5000/chat');

  useEffect(() => {
    start();
    socket.on('response', (response) => {
      setQuestionSubmitted(false);
      console.log(response);
      updateMessage({
        author: 'bot', body: {
          type: MessageType.Text,
          data: response
        }, timeout: 1000
      });
    });

    // Clean up the socket connection when the component unmounts
    return () => {
      socket.disconnect();
    };
  }, []);

  const start = () => {
    setMessages([]);

    initialMessages.forEach((item, index) => {
      setTimeout(() => addMessage(item), item.timeout);
    });

    setTimeout(() => {
      setMessages((prevMessages) => prevMessages.slice(1));
    }, 700);
  };

  const addMessage = (item: ChatMessage) => {
    setMessages((prevMessages) => [...prevMessages, item]);
    const items = document.querySelectorAll('li');
    const lastItem = items[items.length - 1];
    document.querySelector('.c-chat__list')!.scrollTop = lastItem?.offsetTop + lastItem?.clientHeight;
  };

  const updateMessage = (item: ChatMessage) => {
    setMessages((prevMessages) => {
      const arr = [...prevMessages];
      arr[prevMessages.length - 1] = item;
      return arr;
    });
    const items = document.querySelectorAll('li');
    const lastItem = items[items.length - 1];
    document.querySelector('.c-chat__list')!.scrollTop = lastItem?.offsetTop + lastItem?.clientHeight;
  };

  const sendMessage = (message: Body) => {
    if (questionSubmitted) {
      // Do nothing if a question has already been submitted
      return;
    }

    setQuestionSubmitted(true);
    addMessage({
      author: 'bot', body: {
        type: MessageType.Text,
        data: "..."
      }, timeout: 1000
    });
    if (message.type == MessageType.Text) {
      socket.emit("message", message.data);
    } else {
      socket.emit("voice", message.data);
    } // 2 seconds delay before sending the message
  };

  const handleSubmit = (e : any) => {
    e.preventDefault();
    const input = e.target.querySelector('input');

    addMessage({
      author: 'human',
      body: {
        type: MessageType.Text,
        data: input.value
      },
      timeout: 1000
    });

    sendMessage({
      type: MessageType.Text,
      data: input.value
    });

    e.target.reset();
  };

  class CodePostal {
    async save() { }
  }

  const startRecording = () => {
    if (questionSubmitted) {
      return;
    }
    if (isRecording) {
      // If already recording, stop the recording
      stopRecording();
    } else {
      // If not recording, start recording
      navigator.mediaDevices
        .getUserMedia({ audio: true })
        .then((stream) => {
          console.log("HERE NOW")
          mediaRecorder.current = new MediaRecorder(stream);
          const audioChunks: CodePostal[] = [];

          mediaRecorder.current.ondataavailable = (e : any) => {
            if (e.data.size > 0) {
              audioChunks.push(e.data);
            }
          };

          mediaRecorder.current.onstop = () => {
            const audioBlob = new Blob(audioChunks);

            // Convert audioBlob to base64
            const reader = new FileReader();
            reader.onload = (event) => {
              const base64Audio = event.target!.result;
              console.log("NOW UPDATING")
              console.log(base64Audio);
              console.log(typeof (base64Audio));

              setRecordedAudio(base64Audio);
              addMessage({
                author: "human",
                timeout: 1000,
                body: {
                  type: MessageType.Audio,
                  data: base64Audio as string
                }
              })

              sendMessage({
                type: MessageType.Audio,
                data: base64Audio as string
              })

              setIsRecording(false);
              // Send the audioBlob or base64Audio to your backend API
              // sendVoiceToBackend(base64Audio);

            };

            reader.readAsDataURL(audioBlob);
          };

          mediaRecorder.current.start();
          setIsRecording(true);
        })
        .catch((error) => {
          console.error('Error accessing the microphone:', error);
        });
    }
  };

  const stopRecording = () => {
    // if(questionSubmitted) {
    //   return;
    // }
    if (mediaRecorder.current && mediaRecorder.current.state === 'recording') {
      mediaRecorder.current.stop();
      console.log(mediaRecorder)
      setIsRecording(!isRecording);
    }
  };

  let cssClass = ['c-chat'];

  if (messages.length > 0) {
    cssClass.push('c-chat--ready');
  }

  return (
    <div className={cssClass.join(' ')}>
      <ul className="c-chat__list">
        {messages.map((message, index) => <Message key={index} data={message} />)}
      </ul>
      <form className="c-chat__form" onSubmit={handleSubmit}>
        <input
          type="text"
          name="input"
          placeholder="Type your message here..."
          autoFocus
          autoComplete="off"
          required
          disabled={questionSubmitted}
        />
      </form>

      <div className='' onClick={startRecording}>

        <div className="frame">
          <input type="checkbox" name="toggle" id="record-toggle" checked={isRecording} disabled={questionSubmitted} />

          <svg viewBox="0 0 100 100">
            <circle cx="50%" cy="50%" r="45" className="circle-svg" />
          </svg>

          <div className="mic">
            <div className="mic__head"></div>
            <div className="mic__neck"></div>
            <div className="mic__leg"></div>
          </div>

          <div className="recording">
            <div className="round"></div>
            <div className="round"></div>
            <div className="round"></div>
          </div>

          <label htmlFor="record-toggle" className="toggle-label"></label>
        </div>


      </div>
    </div>
  );
};

export default Chat;