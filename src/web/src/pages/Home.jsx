import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";

export const Home = ({ name, handleNameChange }) => {
  const [aboutMeText, setAboutMeText] = useState("");
  const navigate = useNavigate();

  const handleTextAreaChange = (e) => {
    setAboutMeText(e.target.value);
  };

  const onNextClick = () => {
    if (name === "") {
      alert("please input a name");
      return;
    }

    navigate("/chat");
  };

  return (
    <div className="Home">
      <h1>Brock U Chat App</h1>
      <h3>About</h3>
      <p>
        This chat app is designed for brocku students to interact with each
        other, right now it only communicates with the API
      </p>
      <label className="name-input-label">
        <p>Name: </p>
        <input
          value={name}
          onChange={handleNameChange}
          className="name-input"
        />
      </label>
      <button onClick={onNextClick} className="next-btn">
        Next page
      </button>
    </div>
  );
};
