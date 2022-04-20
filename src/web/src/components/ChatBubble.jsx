import "./ChatBubble.css";

const setBubbleColor = (ownedByCurrentUser, brockVer) => {
  var bubbleColor = ownedByCurrentUser ? "current-user" : "not-current-user";
  if (ownedByCurrentUser) {

      console.log(brockVer)

      if (!brockVer) {
          bubbleColor = "current-userCG";
      }

  }
  return `chat-bubble ${bubbleColor}`;
};

export const ChatBubble = ({
  body,
  username,
  timestamp,
  ownedByCurrentUser,
  brockVer,
}) => (
  <div className={setBubbleColor(ownedByCurrentUser, brockVer)}>
    <p>{body}</p>
    <p>{username}</p>
    <p>{timestamp}</p>
  </div>
);
