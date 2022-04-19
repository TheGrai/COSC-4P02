import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./HomeCG.css";

export const HomeCG = ({ name, handleNameChange }) => {
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

    navigate("/chatCG");
  };

  const onSwitchClick = () => {

    document.getElementById("mainApp").classList.remove("AppCG");
    document.getElementById("mainApp").classList.add("App");
    navigate("/");

  };

  return (
    <div className="Home">
      <h1>Canada Games Chat App</h1>
      <h3>About</h3>
      <p>
        This chat app is designed for Canada Games Attendees and others to ask questions about the Niagara 2022 Games
      </p>
      <label className="name-input-label">
        <p>Name: </p>
        <input
          value={name}
          onChange={handleNameChange}
          className="name-input"
        />
      </label>
      <button onClick={onNextClick} className="nextCG-btn">
        Next page
      </button>
      <button onClick={onSwitchClick} className="switch-btn">
        BrockU
      </button>
    </div>
  );
};
