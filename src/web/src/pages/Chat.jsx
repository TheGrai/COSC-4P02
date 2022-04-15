import { useState, useRef, useEffect } from "react";
import { ChatBubble } from "../components/ChatBubble";
import { useNavigate } from "react-router-dom";
import { format } from "date-fns";
import { CSVLink } from "react-csv";

import "./Chat.css";

export const Chat = ({ name }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [latestMessage, setLatestMessage] = useState("");
  const navigate = useNavigate();

  const onInputChange = (e) => {
    setInput(e.target.value);
  };

  const onInputKeyDown = (e) => {
    if (input === "") {
      return;
    }

    if (e.key === "Enter") {
      setLatestMessage(input);
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          body: input,
          username: name,
          timestamp: format(new Date(), "p"),
          ownedByCurrentUser: true,
        },
      ]);
      setInput("");
    }
  };

  const handleSendClick = () => {
    if (input === "") {
      return;
    }

    setLatestMessage(input);
    setMessages((prevMessages) => [
      ...prevMessages,
      {
        body: input,
        username: name,
        timestamp: format(new Date(), "p"),
        ownedByCurrentUser: true,
      },
    ]);
    setInput("");
  };

  const handleHomeClick = () => navigate("/");

  const chatRef = useRef(null);

  const scrollToBottom = () => {
    chatRef.current.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
    });
  };

  const handleCSVClick = () => {
    if (!messages.length) {
      alert("No messages to download");
      return false;
    }
  };

  useEffect(() => {
    // fetch(`http://localhost:2022/chat/?message=${latestMessage}`).then(() => console.log("finish")).then((message) => {
    //   setMessages((prevMessages) => [
    //     ...prevMessages,
    //     {
    //       body: message,
    //       username: "the enemy",
    //       timestamp: format(new Date(), "p"),
    //       ownedByCurrentUser: false,
    //     },
    //   ]);
    // }).catch(() => console.log("error"));
    const getResponse = async() => {
      const results = fetch(`http://localhost:2022/chat/?message=${latestMessage}`)
      console.log(results);
    }
    getResponse();
  }, [latestMessage, setMessages]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (name === "") {
      navigate("/");
    }
  }, [name]);

  return (
    <div className="chat">
      <div className="header">
        <p>Chat room</p>
        <button className="back-btn" onClick={handleHomeClick}>
          Home
        </button>
      </div>
      <div className="chat-container">
        {messages.map((props) => (
          <ChatBubble {...props} />
        ))}
        <div ref={chatRef} />
      </div>
      <div className="input-container">
        <input
          className="chat-input"
          value={input}
          onChange={onInputChange}
          onKeyDown={onInputKeyDown}
        />
        <button onClick={handleSendClick} className="send-btn">
          send
        </button>
        <CSVLink
          data={messages}
          className="send-btn download-csv-btn"
          onClick={handleCSVClick}
        >
          &#8595;
        </CSVLink>
      </div>
    </div>
  );
};