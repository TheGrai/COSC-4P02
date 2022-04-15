import "./ChatBubble.css";

const setBubbleColor = (ownedByCurrentUser) => {
  const bubbleColor = ownedByCurrentUser ? "current-user" : "not-current-user";

  return `chat-bubble ${bubbleColor}`;
};

export const ChatBubble = ({
  body,
  username,
  timestamp,
  ownedByCurrentUser,
}) => (
  <div className={setBubbleColor(ownedByCurrentUser)}>
    <p>{body}</p>
    <p>{username}</p>
    <p>{timestamp}</p>
  </div>
);
