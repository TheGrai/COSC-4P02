import {useState, useRef, useEffect} from "react";
import {ChatBubble} from "../components/ChatBubble";
import {useNavigate} from "react-router-dom";
import {format} from "date-fns";
import {CSVLink} from "react-csv";

import "./ChatCG.css";

    export function useFirstRender() {
        const firstRender = useRef(true);

        useEffect(() => {
            firstRender.current = false;
        }, []);

        return firstRender.current;
    }

export const ChatCG = ({name}) => {
        const firstRender = useFirstRender();
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
                    brockVer: false,
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
                brockVer: false,

            },
        ]);
        setInput("");
    };

    const handleHomeClick = () => navigate("/homeCG");

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

    const handleClearInput = () => {

        setInput("");

    };

    useEffect(() => {
        if(!firstRender){
            const getResponse = async () => {
                fetch(`http://localhost:/api/?cg=${latestMessage}`)
                    .then(response => response.json())
                    .then(data => {
                            setMessages((prevMessages) => [
                                ...prevMessages,
                                {
                                    body: data.message,
                                    username: 'Dr. Bot',
                                    timestamp: format(new Date(), "p"),
                                    ownedByCurrentUser: false,
                                    brockVer: false,
                                },
                            ]);
                            console.log(data.message);
                        }
                    );
            }
            getResponse();

        }
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
                <img src = "niagara.png" height = "75"/>
                <button className="backCG-btn" onClick={handleHomeClick}>
                    Home
                </button>
            </div>
            <div className="chat-container">
                {messages.map((props) => (
                    <ChatBubble {...props} />
                ))}
                <div ref={chatRef}/>
            </div>
            <div className="input-container">
                <button onClick={handleClearInput} className="clear-btn">
                    X
                </button>
                <input
                    className="chat-input"
                    value={input}
                    onChange={onInputChange}
                    onKeyDown={onInputKeyDown}
                />
                <button onClick={handleSendClick} className="sendCG-btn">
                    send
                </button>
                <CSVLink
                    data={messages}
                    className="sendCG-btn download-csv-btn"
                    onClick={handleCSVClick}
                >
                    &#8595;
                </CSVLink>
            </div>
        </div>
    );
};
