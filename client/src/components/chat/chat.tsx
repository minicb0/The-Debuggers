import React, { useState, useEffect } from 'react';
import Typewriter from 'typewriter-effect';
import socketIOClient from 'socket.io-client';
import "./styles.css";

const initialMessages = [
  {
    author: 'bot',
    body: 'Hello',
    timeout: 800
  }
];

const Message = ({ data }) => {
  const { author, body } = data;
  console.log(data)
  let finalBody;

  if (Array.isArray(body)) {
    finalBody = body.map((item, index) => (
      <>
        {item === "..." && (
          <div class="typing">
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
      </>

    ));
  } else {
    if(body === "...") {
      finalBody = <div class="c-chat__message typing"><span></span><span></span><span></span></div>
    } else {
      if(author === "bot") {
        finalBody = <div className="c-chat__message"><Typewriter options={{ strings: body, autoStart: true,delay: 5, loop: false }} /> </div>;
      } else {
        finalBody = <div className="c-chat__message"> {body} </div>;
      }
    }
    
  }

  return (
    <li className={`c-chat__item c-chat__item--${author}`}>
      {finalBody}
    </li>
  );
};

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [questionSubmitted, setQuestionSubmitted] = useState(false);

  const socket = socketIOClient('http://localhost:5000/chat');

  useEffect(() => {
    start();
    socket.on('response', (response) => {
      setQuestionSubmitted(false);
      updateMessage({ author: 'bot', body: response, timeout: 1000 });
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

  const addMessage = (item) => {
    setMessages((prevMessages) => [...prevMessages, item]);
    const items = document.querySelectorAll('li');
    const lastItem = items[items.length - 1];
    document.querySelector('.c-chat__list').scrollTop = lastItem?.offsetTop + lastItem?.clientHeight;
  };

  const updateMessage = (item) => {
    setMessages((prevMessages) => {
      const arr = [...prevMessages];
      arr[prevMessages.length - 1] = item
      return arr
    });
    const items = document.querySelectorAll('li');
    const lastItem = items[items.length - 1];
    document.querySelector('.c-chat__list').scrollTop = lastItem?.offsetTop + lastItem?.clientHeight;
  };

  const sendMessage = (message) => {
    if (questionSubmitted) {
      // Do nothing if a question has already been submitted
      return;
    }

    setQuestionSubmitted(true);
    addMessage({ author: 'bot', body: "...", timeout: 1000 });
    setTimeout(() => {
      socket.emit("message",message);
    }, 2000); // 2 seconds delay before sending the message
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const input = e.target.querySelector('input');

    addMessage({
      author: 'human',
      body: input.value,
    });

    sendMessage(input.value);

    e.target.reset();
  };

  let cssClass = ['c-chat'];

  if (messages.length > 0) {
    cssClass.push('c-chat--ready');
  }

  return (
    <div className={cssClass.join(' ')}>
      <ul className="c-chat__list">
        {messages.map((message, index) => (

          <Message key={index} data={message} />
        ))}
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
    </div>
  );
};

export default Chat;
